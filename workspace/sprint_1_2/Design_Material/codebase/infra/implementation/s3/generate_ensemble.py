#!/usr/bin/env python3
"""Generate a Triton ensemble model repository for the VKIST vision pipeline.

The VKIST design docs define the logical vision flow as:

1. Angle classification selects the scan view.
2. Inflammation detection checks whether synovitis/effusion is present.
3. Segmentation models produce anatomical masks for supported view branches.

The 11 resident Triton models in this repository all consume the same raw image
tensor (`input_image`) and return `logits`. Triton ensemble scheduling moves
those tensors through the ensemble graph internally, so this generator maps the
external client input once and exposes every component model's logits as a
terminal ensemble output.
"""

from __future__ import annotations

import argparse
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable


ENSEMBLE_NAME = "my_vision_pipeline_ensemble"
MODEL_ROOT_DEFAULT = Path(__file__).resolve().parent
OUTPUT_DIR_DEFAULT = Path(__file__).resolve().parent / ENSEMBLE_NAME
VERSION_DIR = "1"

# Ordered by the architecture documents: angle classification -> inflammation
# detection -> segmentation. These are the 11 component models already resident
# under s3://vkist-ml-model/.
ANGLE_CLASSIFICATION_MODELS = [
    "angle_classify_convnext_tiny",
    "angle_classify_resnet50",
    "angle_classify_swin_v2_s",
    "angle_classify_densenet",
    "angle_classify_efficientnet",
]

INFLAMMATION_MODELS = [
    "inflammation_model_efficientnet_b0_ultrasound_2_cls",
]

SEGMENTATION_MODELS = [
    "segmentation_model_unet_resnet101",
    "segmentation_model_unet3plus_att",
    "segmentation_model_post_deeplabv3_resnet101",
    "segmentation_model_post_deeplabv3",
    "segmentation_model_post_efficientfeedback",
]

ALL_MODEL_NAMES = [
    *ANGLE_CLASSIFICATION_MODELS,
    *INFLAMMATION_MODELS,
    *SEGMENTATION_MODELS,
]

DEFAULT_INPUT_NAME = "input"
DEFAULT_INPUT_DATA_TYPE = "TYPE_UINT8"
DEFAULT_INPUT_DIMS = [-1, -1, -1, 3]
DEFAULT_MODEL_INPUT_NAME = "input_image"
DEFAULT_MODEL_OUTPUT_NAME = "logits"
DEFAULT_MODEL_OUTPUT_DATA_TYPE = "TYPE_FP32"
DEFAULT_MAX_BATCH_SIZE = 8


@dataclass(frozen=True)
class ModelConfig:
    """Parsed Triton config for one resident component model."""

    name: str
    platform: str
    max_batch_size: int
    input_name: str
    input_data_type: str
    input_dims: list[int]
    output_name: str
    output_data_type: str
    output_dims: list[int]


@dataclass(frozen=True)
class EnsembleTensor:
    """One ensemble output and its matching internal model-output tensor."""

    model_name: str
    internal_name: str
    output_name: str
    data_type: str
    dims: list[int]


def parse_int_list(text: str) -> list[int]:
    """Parse a Triton dims list such as '[ -1, 7, 512, 512 ]'."""

    return [int(item) for item in re.findall(r"-?\d+", text)]


def parse_scalar(text: str, key: str, default: str | None = None) -> str | None:
    """Parse a quoted scalar from pbtxt text."""

    match = re.search(rf"^\s*{re.escape(key)}:\s*\"([^\"]+)\"", text, flags=re.MULTILINE)
    if match:
        return match.group(1)
    return default


def parse_block_fields(block_text: str) -> dict[str, str]:
    """Parse the simple scalar fields used by the existing model configs."""

    fields: dict[str, str] = {}
    for key in ("name", "platform", "data_type"):
        value = parse_scalar(block_text, key)
        if value is not None:
            fields[key] = value
    return fields


def parse_first_model_config(config_path: Path, fallback_name: str) -> ModelConfig:
    """Parse a component model config.pbtxt and fall back to known defaults."""

    text = config_path.read_text(encoding="utf-8")
    name = parse_scalar(text, "name", fallback_name) or fallback_name
    platform = parse_scalar(text, "platform", "unknown") or "unknown"
    max_batch_match = re.search(r"^\s*max_batch_size:\s*(-?\d+)", text, flags=re.MULTILINE)
    max_batch_size = int(max_batch_match.group(1)) if max_batch_match else DEFAULT_MAX_BATCH_SIZE

    input_match = re.search(r"input\s*\[(.*?)\]\s*output", text, flags=re.DOTALL)
    output_match = re.search(r"output\s*\[(.*?)\]\s*$", text, flags=re.DOTALL)

    input_fields = parse_block_fields(input_match.group(1)) if input_match else {}
    output_fields = parse_block_fields(output_match.group(1)) if output_match else {}

    input_dims_match = re.search(r"dims:\s*\[(.*?)\]", input_match.group(1), flags=re.DOTALL) if input_match else None
    output_dims_match = re.search(r"dims:\s*\[(.*?)\]", output_match.group(1), flags=re.DOTALL) if output_match else None

    input_dims = parse_int_list(input_dims_match.group(1)) if input_dims_match else DEFAULT_INPUT_DIMS
    output_dims = parse_int_list(output_dims_match.group(1)) if output_dims_match else [4]

    return ModelConfig(
        name=name,
        platform=platform,
        max_batch_size=max_batch_size,
        input_name=input_fields.get("name", DEFAULT_MODEL_INPUT_NAME),
        input_data_type=input_fields.get("data_type", DEFAULT_INPUT_DATA_TYPE),
        input_dims=input_dims,
        output_name=output_fields.get("name", DEFAULT_MODEL_OUTPUT_NAME),
        output_data_type=output_fields.get("data_type", DEFAULT_MODEL_OUTPUT_DATA_TYPE),
        output_dims=output_dims,
    )


def load_model_configs(model_root: Path, model_names: Iterable[str]) -> dict[str, ModelConfig]:
    """Load component configs from the local S3 mirror used by Triton."""

    configs: dict[str, ModelConfig] = {}
    for model_name in model_names:
        config_path = model_root / model_name / "config.pbtxt"
        configs[model_name] = parse_first_model_config(config_path, model_name)
    return configs


def tensor_name_for_model(model_name: str) -> str:
    """Create a stable internal ensemble tensor name for one model."""

    return f"{model_name}_logits"


def output_name_for_model(model_name: str) -> str:
    """Create the public ensemble output name for one component model."""

    return model_name.upper()


def ensemble_output_dims(model_config: ModelConfig, max_batch_size: int) -> list[int]:
    """Return non-batch output dims for an ensemble output block.

    Existing component configs include a leading `-1` output dim for dynamic
    batching. Triton ensemble output blocks should declare only non-batch dims
    when `max_batch_size` is positive.
    """

    dims = list(model_config.output_dims)
    if max_batch_size > 0 and dims and dims[0] == -1:
        return dims[1:]
    return dims


def format_dims(dims: Iterable[int]) -> str:
    """Format Triton dims as `[ 7, 512, 512 ]`."""

    return "[ " + ", ".join(str(dim) for dim in dims) + " ]"


def build_ensemble_tensors(
    model_configs: dict[str, ModelConfig],
    max_batch_size: int,
) -> list[EnsembleTensor]:
    """Build ordered public outputs for the ensemble config."""

    tensors: list[EnsembleTensor] = []
    for model_name in ALL_MODEL_NAMES:
        model_config = model_configs[model_name]
        tensors.append(
            EnsembleTensor(
                model_name=model_name,
                internal_name=tensor_name_for_model(model_name),
                output_name=output_name_for_model(model_name),
                data_type=model_config.output_data_type,
                dims=ensemble_output_dims(model_config, max_batch_size),
            )
        )
    return tensors


def format_input_block(input_name: str, input_data_type: str, input_dims: list[int]) -> str:
    """Render the ensemble input block."""

    return f"""    {{
      name: "{input_name}"
      data_type: {input_data_type}
      dims: {format_dims(input_dims)}
    }}"""


def format_output_block(tensor: EnsembleTensor) -> str:
    """Render one ensemble output block."""

    return f"""    {{
      name: "{tensor.output_name}"
      data_type: {tensor.data_type}
      dims: {format_dims(tensor.dims)}
    }}"""


def format_step_block(model_name: str, model_input_name: str, input_value: str, model_output_name: str, output_value: str) -> str:
    """Render one Triton ensemble_scheduling step."""

    return f"""    {{
      model_name: "{model_name}"
      model_version: -1
      input_map {{
        key: "{model_input_name}"
        value: "{input_value}"
      }}
      output_map {{
        key: "{model_output_name}"
        value: "{output_value}"
      }}
    }}"""


def build_config_pbtxt(
    ensemble_name: str,
    max_batch_size: int,
    input_name: str,
    input_data_type: str,
    input_dims: list[int],
    tensors: list[EnsembleTensor],
    model_configs: dict[str, ModelConfig],
) -> str:
    """Build the complete Triton ensemble config.pbtxt string."""

    input_blocks = [format_input_block(input_name, input_data_type, input_dims)]
    output_blocks = [format_output_block(tensor) for tensor in tensors]

    steps: list[str] = []
    for model_name in ALL_MODEL_NAMES:
        model_config = model_configs[model_name]
        tensor = next(item for item in tensors if item.model_name == model_name)
        steps.append(
            format_step_block(
                model_name=model_name,
                model_input_name=model_config.input_name,
                input_value=input_name,
                model_output_name=model_config.output_name,
                output_value=tensor.internal_name,
            )
        )

    sections = [
        f"name: \"{ensemble_name}\"",
        "platform: \"ensemble\"",
        f"max_batch_size: {max_batch_size}",
        "input [\n" + ",\n".join(input_blocks) + "\n]",
        "output [\n" + ",\n".join(output_blocks) + "\n]",
        "ensemble_scheduling {\n  step [\n" + ",\n".join(steps) + "\n  ]\n}",
        "",
    ]
    return "\n".join(sections)


def parse_dims_arg(value: str) -> list[int]:
    """Parse a comma-separated dims CLI value."""

    return [int(item.strip()) for item in value.split(",") if item.strip()]


def prepare_output_dir(output_dir: Path, clean: bool) -> None:
    """Create or refresh the local Triton model repository directory."""

    if clean and output_dir.exists():
        import shutil

        shutil.rmtree(output_dir)
    version_dir = output_dir / VERSION_DIR
    version_dir.mkdir(parents=True, exist_ok=True)


def generate_ensemble(
    model_root: Path,
    output_dir: Path,
    ensemble_name: str,
    max_batch_size: int,
    input_name: str,
    input_data_type: str,
    input_dims: list[int],
    clean: bool,
) -> Path:
    """Generate the ensemble repository and return the written config path."""

    model_configs = load_model_configs(model_root, ALL_MODEL_NAMES)
    tensors = build_ensemble_tensors(model_configs, max_batch_size)
    config_text = build_config_pbtxt(
        ensemble_name=ensemble_name,
        max_batch_size=max_batch_size,
        input_name=input_name,
        input_data_type=input_data_type,
        input_dims=input_dims,
        tensors=tensors,
        model_configs=model_configs,
    )

    prepare_output_dir(output_dir, clean=clean)
    config_path = output_dir / VERSION_DIR / "config.pbtxt"
    config_path.write_text(config_text, encoding="utf-8")
    return config_path


def build_arg_parser() -> argparse.ArgumentParser:
    """Build CLI arguments for local generation."""

    parser = argparse.ArgumentParser(
        description="Generate Triton ensemble config for the VKIST 11-model vision pipeline."
    )
    parser.add_argument(
        "--model-root",
        type=Path,
        default=MODEL_ROOT_DEFAULT,
        help="Local directory containing the 11 resident model config.pbtxt files.",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=OUTPUT_DIR_DEFAULT,
        help="Local Triton model repository directory to create.",
    )
    parser.add_argument(
        "--ensemble-name",
        default=ENSEMBLE_NAME,
        help="Triton ensemble model name and S3 top-level folder name.",
    )
    parser.add_argument(
        "--max-batch-size",
        type=int,
        default=DEFAULT_MAX_BATCH_SIZE,
        help="Triton max_batch_size for the ensemble.",
    )
    parser.add_argument(
        "--input-name",
        default=DEFAULT_INPUT_NAME,
        help="External client input tensor name.",
    )
    parser.add_argument(
        "--input-data-type",
        default=DEFAULT_INPUT_DATA_TYPE,
        help="External client input tensor data type.",
    )
    parser.add_argument(
        "--input-dims",
        default=",".join(str(item) for item in DEFAULT_INPUT_DIMS),
        help="Comma-separated external input dims, excluding batch dimension.",
    )
    parser.add_argument(
        "--no-clean",
        action="store_true",
        help="Do not remove an existing output directory before generation.",
    )
    return parser


def main() -> None:
    """CLI entry point."""

    args = build_arg_parser().parse_args()
    config_path = generate_ensemble(
        model_root=args.model_root,
        output_dir=args.output_dir,
        ensemble_name=args.ensemble_name,
        max_batch_size=args.max_batch_size,
        input_name=args.input_name,
        input_data_type=args.input_data_type,
        input_dims=parse_dims_arg(args.input_dims),
        clean=not args.no_clean,
    )
    print(f"Wrote Triton ensemble config: {config_path}")


if __name__ == "__main__":
    main()
