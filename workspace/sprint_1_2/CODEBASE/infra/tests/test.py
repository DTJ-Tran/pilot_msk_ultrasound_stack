import os
import sys
import json
import base64
import io
import time
from pathlib import Path
import numpy as np
from PIL import Image
import requests


TRITON_URL = "https://dtj-tran--triton-s3-service-unified-triton-server.modal.run"
MODEL_NAME = "msk_vision_pipeline_ensemble"

BASE_DIR = Path(__file__).resolve().parent
TEST_IMAGE_DIR = BASE_DIR / "test_images"

ANGLE_CLASSES = ["med-lat", "post-trans", "sup-trans-flex", "sup-up-long"]

ANGLE_OUTPUT_NAMES = [
    "angle_classify_convnext_tiny_logits",
    "angle_classify_resnet50_logits",
    "angle_classify_swin_v2_s_logits",
    "angle_classify_densenet_logits",
    "angle_classify_efficientnet_logits",
]

SUP_SEG_OUTPUT_NAMES = [
    "segmentation_model_unet_resnet101_logits",
    "segmentation_model_unet3plus_att_logits",
]

POST_SEG_OUTPUT_NAMES = [
    "segmentation_model_post_deeplabv3_resnet101_logits",
    "segmentation_model_post_deeplabv3_logits",
    "segmentation_model_post_efficientfeedback_logits",
]


def load_image(path: Path) -> Image.Image:
    return Image.open(path).convert("RGB")


def preprocess_224(img: Image.Image) -> np.ndarray:
    img_resized = img.resize((224, 224), Image.Resampling.BILINEAR)
    arr = np.asarray(img_resized).astype(np.float32) / 255.0
    mean = np.array([0.485, 0.456, 0.406], dtype=np.float32)
    std = np.array([0.229, 0.224, 0.225], dtype=np.float32)
    arr = (arr - mean) / std
    arr = arr.transpose(2, 0, 1)  # HWC -> CHW
    arr = np.expand_dims(arr, axis=0)  # NCHW
    return arr


def preprocess_512(img: Image.Image) -> np.ndarray:
    img_resized = img.resize((512, 512), Image.Resampling.BILINEAR)
    arr = np.asarray(img_resized).astype(np.float32) / 255.0
    arr = arr.transpose(2, 0, 1)  # HWC -> CHW
    arr = np.expand_dims(arr, axis=0)  # NCHW
    return arr

def build_ensemble_request(input_224: np.ndarray, input_512: np.ndarray, model_name: str) -> tuple[bytes, dict]:
    inputs = [
        {
            "name": "input_224",
            "shape": list(input_224.shape),
            "datatype": "FP32",
            "parameters": {"binary_data_size": input_224.nbytes},
        },
        {
            "name": "input_512",
            "shape": list(input_512.shape),
            "datatype": "FP32",
            "parameters": {"binary_data_size": input_512.nbytes},
        },
    ]
    outputs = [
        {"name": name}
        for name in (
            ANGLE_OUTPUT_NAMES
            + ["inflammation_model_efficientnet_b0_ultrasound_2_cls_logits"]
            + SUP_SEG_OUTPUT_NAMES
            + POST_SEG_OUTPUT_NAMES
        )
    ]

    metadata = {"model_name": model_name, "model_version": "", "inputs": inputs, "outputs": outputs}
    metadata_bytes = json.dumps(metadata).encode("utf-8")

    body = metadata_bytes + input_224.tobytes() + input_512.tobytes()
    headers = {"Inference-Header-Content-Length": str(len(metadata_bytes)), "Content-Type": "application/octet-stream"}
    return body, headers

def parse_kserve_v2_response(resp: requests.Response) -> dict:
    # 1. Pull the header length sent by Triton
    header_length = int(resp.headers.get("Inference-Header-Content-Length", "0"))
    response_bytes = resp.content
    
    # 2. Extract the JSON metadata section
    metadata = json.loads(response_bytes[:header_length].decode("utf-8"))
    binary_data = response_bytes[header_length:]

    # Dictionary to map Triton datatypes to numpy types & byte sizes
    dtype_map = {
        "FP32": (np.float32, 4),
        "INT32": (np.int32, 4),
        "INT64": (np.int64, 8),
        "FP16": (np.float16, 2),
        "UINT8": (np.uint8, 1)
    }

    result = {"metadata": metadata, "outputs": {}}
    offset = 0
    
    for desc in metadata.get("outputs", []):
        name = desc["name"]
        shape = desc["shape"]
        datatype = desc["datatype"]
        
        # Determine the data type and total size safely
        np_type, element_size = dtype_map.get(datatype, (np.float32, 4))
        total_elements = int(np.prod(shape))
        
        # SAFE EXTRACT: Look for 'binary_data_size'. 
        # If it's missing (common in ensemble nodes), calculate it manually!
        params = desc.get("parameters", {})
        size = params.get("binary_data_size", total_elements * element_size)
        
        # Extract the slice of raw bytes
        raw = binary_data[offset : offset + size]
        
        # Convert raw buffer back into a structured NumPy array
        arr = np.frombuffer(raw, dtype=np_type).reshape(shape)
        result["outputs"][name] = arr
        
        # Move our index cursor forward
        offset += size
        
    return result


def softmax(x: np.ndarray) -> np.ndarray:
    e = np.exp(x - np.max(x))
    return e / np.sum(e)


def decode_angle_from_ensemble(outputs: dict) -> tuple[str, float]:
    logits_list = [outputs[name] for name in ANGLE_OUTPUT_NAMES if name in outputs]
    if not logits_list:
        raise ValueError("No angle logits found in ensemble outputs")
    
    # stack and average across models
    avg_logits = np.mean(np.stack(logits_list), axis=0)
    # remove batch dimension if present
    if avg_logits.ndim > 1 and avg_logits.shape[0] == 1:
        avg_logits = avg_logits[0]
    probs = softmax(avg_logits)
    idx = int(np.argmax(probs))
    return ANGLE_CLASSES[idx], float(probs[idx])


def decode_inflammation(outputs: dict) -> tuple[bool, float]:
    key = "inflammation_model_efficientnet_b0_ultrasound_2_cls_logits"
    logits = outputs[key]
    probs = softmax(logits)
    prob_inflam = float(probs[1])
    return bool(prob_inflam >= 0.5), prob_inflam


def infer_ensemble(image: Image.Image) -> dict:
    input_224 = preprocess_224(image)
    input_512 = preprocess_512(image)
    body, headers = build_ensemble_request(input_224, input_512, MODEL_NAME)
    resp = requests.post(
        f"{TRITON_URL}/v2/models/{MODEL_NAME}/infer",
        data=body,
        headers=headers,
        timeout=120,
    )
    resp.raise_for_status()
    if resp.status_code != 200:
        raise RuntimeError(f"Failed to get inference response: {resp.status_code} {resp.text}")
    else:
        print(f"Received inference response: {resp.status_code}")
    return parse_kserve_v2_response(resp)


def analyze_image_flow(image: Image.Image) -> dict:
    t0 = time.time()
    parsed = infer_ensemble(image)
    outputs = parsed["outputs"]

    angle, angle_conf = decode_angle_from_ensemble(outputs)
    print(f"Angle: {angle} ({angle_conf*100:.2f}%)")

    result = {
        "angle": {"class": angle, "confidence": round(angle_conf * 100, 2)},
        "inflammation": None,
        "segmentation": None,
        "measurement": None,
        "severity": None,
    }

    if "post-trans" in angle.lower():
        has_inflammation, inflam_conf = decode_inflammation(outputs)
        result["inflammation"] = {"detected": has_inflammation, "confidence": round(inflam_conf * 100, 2)}
        print(f"Inflammation POST: {has_inflammation} ({result['inflammation']['confidence']}%)")
    elif "sup-up-long" in angle.lower():
        has_inflammation, inflam_conf = decode_inflammation(outputs)
        result["inflammation"] = {"detected": has_inflammation, "confidence": round(inflam_conf * 100, 2)}
        print(f"Inflammation SUP: {has_inflammation} ({result['inflammation']['confidence']}%)")

    elapsed = time.time() - t0
    print(f"Elapsed: {elapsed:.2f}s")
    return result


def main():
    print(f"TRITON_URL={TRITON_URL}")
    print(f"MODEL_NAME={MODEL_NAME}")
    print(f"TEST_IMAGE_DIR={TEST_IMAGE_DIR}")
    print("=" * 60)

    folders = {
        # "sup-up-long_positive": TEST_IMAGE_DIR / "sup-up-long_positive",
        # "sup-up-long_negative": TEST_IMAGE_DIR / "sup-up-long_negative",
        # "post_trans_positive": TEST_IMAGE_DIR / "post_trans_positive",
        # "post_trans_negative": TEST_IMAGE_DIR / "post_trans_negative",
        "other_angle": TEST_IMAGE_DIR / "other_angle",
    }

    summary = []
    for category, folder in folders.items():
        if not folder.exists():
            continue
        for img_path in sorted(folder.iterdir()):
            if img_path.suffix.lower() not in {".jpg", ".jpeg", ".png"}:
                continue
            print(f"\n>>> {category}: {img_path.name}")
            try:
                img = load_image(img_path)
                res = analyze_image_flow(img)
                res["file"] = str(img_path.relative_to(BASE_DIR))
                res["category"] = category
                summary.append(res)
            except Exception as e:
                print(f"Error: {e}")
                import traceback
                traceback.print_exc()
                summary.append({"file": str(img_path.relative_to(BASE_DIR)), "category": category, "error": str(e)})

    out_path = BASE_DIR / "result.json"
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2, ensure_ascii=False)
    print(f"\nSaved results to {out_path}")


if __name__ == "__main__":
    main()
