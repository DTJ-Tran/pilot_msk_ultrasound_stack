import json
import time
from pathlib import Path
import numpy as np
from PIL import Image
import requests

# Server configuration
TRITON_URL = "https://dtj-tran--triton-s3-service-unified-triton-server.modal.run"
TARGET_MODEL = "workspace/sprint_1_2/CODEBASE/infra/tests/models/efficientnet_b0_ultrasound_2_class.pth"  # Target a single sub-model directly
IMFLAMMATION_CLASSES = ["Không viêm", "Có viêm"]

BASE_DIR = Path(__file__).resolve().parent


def load_image(path: Path) -> Image.Image:
    if not path.exists():
        raise FileNotFoundError(f"Test image not found at: {path}")
    return Image.open(path).convert("RGB")


def preprocess_224(img: Image.Image) -> np.ndarray:
    """Preprocesses image to NCHW FP32 [1, 3, 224, 224] matching ResNet50 input requirements"""
    img_resized = img.resize((224, 224), Image.Resampling.BILINEAR)
    arr = np.asarray(img_resized).astype(np.float32) / 255.0
    mean = np.array([0.485, 0.456, 0.406], dtype=np.float32)
    std = np.array([0.229, 0.224, 0.225], dtype=np.float32)
    arr = (arr - mean) / std
    arr = arr.transpose(2, 0, 1)  # HWC -> CHW
    arr = np.expand_dims(arr, axis=0)  # Add batch dim -> NCHW
    return arr


def softmax(x: np.ndarray) -> np.ndarray:
    e = np.exp(x - np.max(x))
    return e / np.sum(e)

def build_binary_request(input_tensor: np.ndarray, model_name: str) -> tuple[bytes, dict]:
    """Constructs a strict KServe v2 binary payload for a single input tensor"""
    # NOTE: Check your individual model's config.pbtxt to verify if the
    # expected input name is 'input_image', 'input_0', etc.
    input_name = "input_image"

    inputs = [
        {
            "name": input_name,
            "shape": list(input_tensor.shape),
            "datatype": "FP32",
            "parameters": {"binary_data_size": input_tensor.nbytes},
        }
    ]

    # We request the standard 'logits' output tensor from this model
    outputs = [{"name": "logits"}]

    metadata = {
        "model_name": model_name,
        "model_version": "",
        "inputs": inputs,
        "outputs": outputs
    }

    metadata_bytes = json.dumps(metadata).encode("utf-8")
    body = metadata_bytes + input_tensor.tobytes()

    headers = {
        "Inference-Header-Content-Length": str(len(metadata_bytes)),
        "Content-Type": "application/octet-stream"
    }
    return body, headers

def parse_binary_response(resp: requests.Response) -> np.ndarray:
    """Parses Triton's binary response stream for a single output tensor"""
    header_length = int(resp.headers.get("Inference-Header-Content-Length", "0"))
    response_bytes = resp.content

    metadata = json.loads(response_bytes[:header_length].decode("utf-8"))
    binary_data = response_bytes[header_length:]

    # Extract the first available output tensor
    output_desc = metadata["outputs"][0]
    shape = output_desc["shape"]

    # Unpack raw bytes back into numpy array
    arr = np.frombuffer(binary_data, dtype=np.float32).reshape(shape)
    return arr

def main():
    # Define a path to a real local image to test with
    image_path = "test_images/sup-up-long_positive/58e7a7ef-de3e-11ee-97e2-0a580a5f5b60_11.png"

    print(f"Targeting Individual Model: {TARGET_MODEL}")
    print(f"Loading image from: {image_path}")

    try:
        # 1. Prepare image
        img = load_image(image_path)
        input_data = preprocess_224(img)

        # 2. Build the payload
        body, headers = build_binary_request(input_data, TARGET_MODEL)

        # 3. Fire request to the targeted model endpoint
        url = f"{TRITON_URL}/v2/models/{TARGET_MODEL}/infer"
        print("Sending request to Triton server...")

        t0 = time.time()
        resp = requests.post(url, data=body, headers=headers, timeout=30)
        resp.raise_for_status()
        latency = time.time() - t0

        # 4. Parse output logits
        logits = parse_binary_response(resp)
        logits = np.squeeze(logits)  # Drop batch dimension

        # 5. Decode probabilities
        probs = softmax(logits)
        predicted_idx = int(np.argmax(probs))

        print("\n" + "=" * 40)
        print("🎉 SUCCESSFUL INFERENCE")
        print(f"Network Roundtrip Time: {latency:.4f}s")
        print("-" * 40)
        print("Class Probabilities:")
        for cls_name, prob in zip(IMFLAMMATION_CLASSES, probs):
            print(f"  {cls_name:<15}: {prob * 100:.2f}%")
        print("-" * 40)
        print(f"Prediction: {IMFLAMMATION_CLASSES[predicted_idx]} ({probs[predicted_idx] * 100:.2f}%)")
        print("=" * 40)

    except Exception as e:
        print(f"\n❌ Inference Failed: {e}")
        if 'resp' in locals() and hasattr(resp, 'text'):
            print(f"Server Error Message: {resp.text}")


if __name__ == "__main__":
    main()