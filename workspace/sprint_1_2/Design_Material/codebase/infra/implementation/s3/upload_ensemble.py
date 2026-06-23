#!/usr/bin/env python3
"""Upload the generated Triton ensemble repository to AWS S3.

This script mirrors the local Triton model repository folder into the active
VKIST model bucket root:

    s3://vkist-ml-model/my_vision_pipeline_ensemble/

It uploads every file and also creates zero-byte directory marker objects so the
S3 prefix reflects the same nested structure Triton expects in a model
repository.
"""

from __future__ import annotations

import argparse
import mimetypes
import os
from pathlib import Path
from typing import Iterable

try:
    import boto3
    from boto3.s3.transfer import TransferConfig
except ImportError:  # pragma: no cover - exercised only when boto3 is absent.
    boto3 = None
    TransferConfig = None


ENSEMBLE_NAME = "my_vision_pipeline_ensemble"
DEFAULT_SOURCE_DIR = Path(__file__).resolve().parent / ENSEMBLE_NAME
DEFAULT_BUCKET_URI = "s3://vkist-ml-model/"
DEFAULT_TRANSFER_CONFIG = None


def require_env(name: str) -> str:
    """Read a required AWS credential/environment value."""

    value = os.environ.get(name)
    if not value:
        raise RuntimeError(f"Missing required environment variable: {name}")
    return value


def parse_s3_uri(uri: str) -> tuple[str, str]:
    """Parse an S3 URI into bucket and prefix."""

    if not uri.startswith("s3://"):
        raise ValueError(f"S3 URI must start with 's3://': {uri}")

    body = uri.removeprefix("s3://").strip()
    if not body:
        raise ValueError("S3 URI must include a bucket name.")

    parts = body.split("/", 1)
    bucket = parts[0]
    prefix = parts[1] if len(parts) > 1 else ""
    return bucket, normalize_prefix(prefix)


def normalize_prefix(prefix: str) -> str:
    """Ensure an S3 prefix ends with '/' when non-empty."""

    prefix = prefix.strip().replace("\\", "/")
    if prefix and not prefix.endswith("/"):
        return prefix + "/"
    return prefix


def relpath_for(path: Path, root: Path) -> Path:
    """Return a POSIX-style relative path under a root directory."""

    return path.relative_to(root).as_posix()


def collect_local_tree(source_dir: Path) -> tuple[list[Path], list[Path]]:
    """Collect local files and directories to mirror into S3."""

    if not source_dir.exists():
        raise FileNotFoundError(f"Source directory does not exist: {source_dir}")
    if not source_dir.is_dir():
        raise NotADirectoryError(f"Source path is not a directory: {source_dir}")

    files = [path for path in source_dir.rglob("*") if path.is_file()]
    directories = [path for path in source_dir.rglob("*") if path.is_dir()]
    directories.append(source_dir)
    return sorted(files), sorted(directories, reverse=True)


def file_key_for(source_dir: Path, file_path: Path, prefix: str) -> str:
    """Build the S3 object key for a local file."""

    return prefix + relpath_for(file_path, source_dir).replace("\\", "/")


def directory_marker_key_for(source_dir: Path, directory_path: Path, prefix: str) -> str:
    """Build the S3 directory marker key for a local directory."""

    if directory_path == source_dir:
        return prefix
    return prefix + relpath_for(directory_path, source_dir).replace("\\", "/") + "/"


def content_type_for(path: Path) -> str:
    """Guess a safe MIME type for an S3 object."""

    guessed_type, _ = mimetypes.guess_type(str(path))
    return guessed_type or "application/octet-stream"


def create_s3_client() -> object:
    """Create a Boto3 S3 client from local AWS environment variables."""

    if boto3 is None:
        raise RuntimeError("boto3 is required. Install it with: pip install boto3")

    access_key = require_env("AWS_ACCESS_KEY_ID")
    secret_key = require_env("AWS_SECRET_ACCESS_KEY")

    client_kwargs = {
        "aws_access_key_id": access_key,
        "aws_secret_access_key": secret_key,
    }

    session_token = os.environ.get("AWS_SESSION_TOKEN")
    if session_token:
        client_kwargs["aws_session_token"] = session_token

    region = os.environ.get("AWS_REGION") or os.environ.get("AWS_DEFAULT_REGION")
    if region:
        client_kwargs["region_name"] = region

    endpoint_url = os.environ.get("AWS_ENDPOINT_URL")
    if endpoint_url:
        client_kwargs["endpoint_url"] = endpoint_url

    return boto3.client("s3", **client_kwargs)


def put_directory_marker(
    s3_client: object,
    bucket: str,
    key: str,
    dry_run: bool = False,
) -> None:
    """Create a zero-byte S3 marker object for one directory prefix."""

    if dry_run:
        print(f"[dry-run] marker s3://{bucket}/{key}")
        return

    s3_client.put_object(
        Bucket=bucket,
        Key=key,
        Body=b"",
        ContentType="application/x-directory",
    )


def upload_file(
    s3_client: object,
    bucket: str,
    local_path: Path,
    key: str,
    transfer_config: TransferConfig | None,
    dry_run: bool = False,
) -> None:
    """Upload one local file to S3."""

    if dry_run:
        print(f"[dry-run] upload {local_path} -> s3://{bucket}/{key}")
        return

    if transfer_config is None:
        if TransferConfig is None:
            raise RuntimeError("boto3 is required. Install it with: pip install boto3")
        transfer_config = TransferConfig(
            multipart_threshold=64 * 1024 * 1024,
            multipart_chunksize=16 * 1024 * 1024,
            max_concurrency=8,
            use_threads=True,
        )

    s3_client.upload_file(
        Filename=str(local_path),
        Bucket=bucket,
        Key=key,
        ExtraArgs={
            "ContentType": content_type_for(local_path),
            "CacheControl": "no-store",
        },
        Config=transfer_config,
    )


def list_existing_keys(s3_client: object, bucket: str, prefix: str) -> set[str]:
    """List all existing object keys below an S3 prefix."""

    paginator = s3_client.get_paginator("list_objects_v2")
    keys: set[str] = set()

    for page in paginator.paginate(Bucket=bucket, Prefix=prefix):
        for item in page.get("Contents", []):
            keys.add(item["Key"])

    return keys


def delete_stale_keys(
    s3_client: object,
    bucket: str,
    prefix: str,
    desired_keys: Iterable[str],
    dry_run: bool = False,
) -> int:
    """Delete objects under the prefix that are not present locally."""

    desired = set(desired_keys)
    existing = list_existing_keys(s3_client, bucket, prefix)
    stale = sorted(existing - desired)

    if not stale:
        return 0

    if dry_run:
        for key in stale:
            print(f"[dry-run] delete s3://{bucket}/{key}")
        return len(stale)

    for key in stale:
        s3_client.delete_object(Bucket=bucket, Key=key)

    return len(stale)


def mirror_to_s3(
    source_dir: Path,
    bucket_uri: str,
    prefix: str | None = None,
    delete: bool = False,
    dry_run: bool = False,
) -> dict[str, int]:
    """Mirror a local Triton model repository directory into S3."""

    bucket, bucket_prefix = parse_s3_uri(bucket_uri)
    effective_prefix = normalize_prefix(prefix if prefix is not None else source_dir.name + "/")
    s3_prefix = bucket_prefix + effective_prefix

    files, directories = collect_local_tree(source_dir)
    s3_client = create_s3_client() if (not dry_run) or delete else None

    desired_keys: set[str] = set()

    for directory_path in directories:
        key = directory_marker_key_for(source_dir, directory_path, s3_prefix)
        desired_keys.add(key)
        put_directory_marker(s3_client, bucket, key, dry_run=dry_run)

    for file_path in files:
        key = file_key_for(source_dir, file_path, s3_prefix)
        desired_keys.add(key)
        upload_file(
            s3_client=s3_client,
            bucket=bucket,
            local_path=file_path,
            key=key,
            transfer_config=DEFAULT_TRANSFER_CONFIG,
            dry_run=dry_run,
        )

    deleted = 0
    if delete:
        deleted = delete_stale_keys(
            s3_client=s3_client,
            bucket=bucket,
            prefix=s3_prefix,
            desired_keys=desired_keys,
            dry_run=dry_run,
        )

    return {
        "files_uploaded": len(files),
        "directories_marked": len(directories),
        "keys_desired": len(desired_keys),
        "keys_deleted": deleted,
    }


def build_arg_parser() -> argparse.ArgumentParser:
    """Build CLI arguments for S3 upload."""

    parser = argparse.ArgumentParser(
        description="Mirror a generated Triton ensemble repository to AWS S3."
    )
    parser.add_argument(
        "--source-dir",
        type=Path,
        default=DEFAULT_SOURCE_DIR,
        help="Local generated Triton model repository directory.",
    )
    parser.add_argument(
        "--bucket-uri",
        default=DEFAULT_BUCKET_URI,
        help="S3 model bucket root URI, for example s3://vkist-ml-model/.",
    )
    parser.add_argument(
        "--prefix",
        default=None,
        help="Optional S3 prefix under the bucket. Defaults to the source folder name.",
    )
    parser.add_argument(
        "--delete",
        action="store_true",
        help="Delete stale objects under the target prefix that are missing locally.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print S3 actions without writing or deleting objects.",
    )
    return parser


def main() -> None:
    """CLI entry point."""

    args = build_arg_parser().parse_args()
    summary = mirror_to_s3(
        source_dir=args.source_dir,
        bucket_uri=args.bucket_uri,
        prefix=args.prefix,
        delete=args.delete,
        dry_run=args.dry_run,
    )

    print(
        "Uploaded ensemble mirror: "
        f"files={summary['files_uploaded']}, "
        f"directories={summary['directories_marked']}, "
        f"desired_keys={summary['keys_desired']}, "
        f"deleted={summary['keys_deleted']}"
    )


if __name__ == "__main__":
    main()
