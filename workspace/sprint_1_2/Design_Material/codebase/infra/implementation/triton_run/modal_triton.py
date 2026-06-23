import subprocess
import modal
import time

# run from root: vkist_internship (will manaage later)

triton_image = (
    modal.Image.from_registry(
        tag="nvcr.io/nvidia/tritonserver:24.02-py3",
        add_python="3.12"
    )
    # Step B: Install minimal system dependencies (replacing your apt-get RUN command)
    .apt_install(
        "libgl1",
        "libglib2.0-0"  # Crucial runtime hook for OpenCV / Ultralytics
    )
    # Step C: Install PyTorch pinned strictly to CUDA 12.1 wheel indices
    .run_commands(
        "python3 -m pip install --upgrade pip setuptools",
        "python3 -m pip install torch==2.5.0 torchaudio==2.5.0 torchvision==0.20.0 --index-url https://download.pytorch.org/whl/cu121",
        "python3 -m pip install transformers==4.57.3 timm==1.0.22 ultralytics==8.3.0 opencv-python grpcio protobuf",
        "python3 -m pip install fastapi[standard]",
        "python3 -m pip install tritonclient[http,cuda]"
    )
)

app = modal.App("triton-s3-service", image=triton_image)
from fastapi import FastAPI, Response, Request,HTTPException
from fastapi.responses import StreamingResponse # 👈 ADD THIS IMPORT
import httpx
web_app = FastAPI()
# -------------------------------------------------------------
# FASTAPI PROXY ROUTING (Living inside the container)
# -------------------------------------------------------------

@web_app.get("/v2/health/ready")
async def forward_health():
    """Proxies external HTTP REST calls straight to Triton's internal inference engine"""
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get("http://127.0.0.1:8000/v2/health/ready")
            return Response(content=response.content, status_code=response.status_code, media_type=response.headers.get("content-type"))
        except Exception as e:
            return Response(content=f"Triton booting models from S3... Error: {str(e)}", status_code=503)

@web_app.get("/metrics")
@web_app.get("/")
async def forward_metrics():
    """Proxies external metric calls straight to Triton's internal metrics engine"""
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get("http://127.0.0.1:8002/metrics")
            return Response(content=response.content, status_code=response.status_code, media_type=response.headers.get("content-type"))
        except Exception as e:
            return Response(content=f"Waiting for metrics channel... Error: {str(e)}", status_code=503)

# 👇 ADD THIS CATCH-ALL ROUTE HERE 👇
@web_app.api_route("/v2/{path:path}", methods=["GET", "POST"])
async def proxy_all_triton_request(path: str, request: Request):
    import tritonclient.grpc.aio as grpcclient 
    from tritonclient.grpc import service_pb2, service_pb2_grpc
    from tritonclient.grpc import _utils as grpc_utils #InferenceServerClient 
    import grpc 
    import numpy as np
    # 1. Keep HTTP proxy ONLY for metadata/health checks
    if "infer" not in path:
        async with httpx.AsyncClient(timeout=60.0) as client:
            url = f"http://127.0.0.1:8000/v2/{path}"
            headers = dict(request.headers)
            headers.pop("host", None)
            triton_response = await client.request(
                method=request.method, url=url, headers=headers, content=await request.body()
            )
            return Response(
                content=triton_response.content, 
                status_code=triton_response.status_code,
                headers=dict(triton_response.headers)
            )
    
    # 2. 🚀 FOR INFERENCE: Convert the incoming HTTP raw body into a gRPC call
    if "infer" in path:
        try:
            # Extract model name from the route path (e.g., v2/models/MODEL_NAME/infer)
            parts = path.split("/")
            model_name = parts[parts.index("models") + 1]
            
            # Read incoming raw binary HTTP payload
            raw_http_body = await request.body()
            
            header_length_str = request.headers.get("Inference-Header-Content-Length")
            if not header_length_str:
                raise HTTPException(
                    status_code=400,
                    detail="Missing 'Inference-Header-Content-Length' header required for binary Triton transcoding."
                )

            header_length = int(header_length_str)

            # --- 💥 KSERVE V2 MULTI-PART BODY PARSING ---
            # Extract the front JSON metadata and the trailing raw binary tensors
            import json
            json_bytes = raw_http_body[:header_length]
            binary_data = raw_http_body[header_length:]
            request_metadata = json.loads(json_bytes.decode('utf-8'))

            # Setup async gRPC connection
            triton_url = "127.0.0.1:8001"

            # Configure channels to accept large payload returns (100MB limit override)
            max_msg_length = 100 * 1024 * 1024 
            channel_options = [
                ('grpc.max_receive_message_length', max_msg_length),
                ('grpc.max_send_message_length', max_msg_length),
            ]
            async with grpc.aio.insecure_channel(triton_url, options=channel_options) as channel:
                stub = service_pb2_grpc.GRPCInferenceServiceStub(channel=channel)

                # Construct the native ModelInferRequest protobuf
                grpc_request = service_pb2.ModelInferRequest()
                grpc_request.model_name = model_name
                grpc_request.model_version = "" 

                # Populate inputs dynamically from incoming KServe metadata
                binary_offset = 0
                for input_tensor in request_metadata.get("inputs", []):
                    # Correct Protobuf repeated field instantiation via .add()
                    infer_input = grpc_request.inputs.add()
                    infer_input.name = input_tensor["name"]
                    infer_input.datatype = input_tensor["datatype"]
                    infer_input.shape.extend(input_tensor["shape"]) # Explicit clean integers!
                    
                    # Extract the binary slice matching this tensor out of the raw payload block
                    if "parameters" in input_tensor and "binary_data_size" in input_tensor["parameters"]:
                        data_size = input_tensor["parameters"]["binary_data_size"]
                        grpc_request.raw_input_contents.append(
                            binary_data[binary_offset : binary_offset + data_size]
                        )
                        binary_offset += data_size

                # Request output tensor mappings dynamically based on what the client requested
                for output_tensor in request_metadata.get("outputs", []):
                    infer_output = grpc_request.outputs.add()
                    infer_output.name = output_tensor["name"]
                    # Signal Triton to return output via raw binary buffers
                    infer_output.parameters["binary_data"].bool_param = True

                # ✅ Send the transcoding payload straight into Triton over internal gRPC loop
                grpc_response = await stub.ModelInfer(request=grpc_request, timeout=None)

            # --- 💥 TRANSCODE gRPC RESPONSE BACK TO MULTI-PART KSERVE HTTP ---
            response_metadata = {
                "model_name": grpc_response.model_name,
                "model_version": grpc_response.model_version,
                "outputs": []
            }
            
            response_binary_body = b""
            for i, output in enumerate(grpc_response.outputs):
                out_desc = {
                    "name": output.name,
                    "datatype": output.datatype,
                    "shape": list(output.shape),
                    "parameters": {
                        "binary_data_size": len(grpc_response.raw_output_contents[i])
                    }
                }
                response_metadata["outputs"].append(out_desc)
                response_binary_body += grpc_response.raw_output_contents[i]

            # Re-bundle into [JSON metadata] + [Raw binary output chunks]
            response_json_bytes = json.dumps(response_metadata).encode('utf-8')
            output_http_body = response_json_bytes + response_binary_body
            
            return Response(
                content=output_http_body,
                status_code=200,
                headers={
                    "Content-Type": "application/octet-stream",
                    "Inference-Header-Content-Length": str(len(response_json_bytes))
                }
            )
        
        except Exception as e:
            import traceback
            print(f"CRITICAL TRANSLATION EXCEPTION: {traceback.format_exc()}")
            return Response(
                content=f"Internal gRPC Pipeline Multiplex Error: {str(e)}", 
                status_code=502
            )

# -------------------------------------------------------------
# THE UNIFIED SERVICE FUNCTION (1 Container, 1 GPU, 1 Triton Process)
# -------------------------------------------------------------

@app.function(
    gpu="T4", # for the expense
    timeout=3600,
    max_containers=3, # Strict production capping
    min_containers=1, # for keeping warm and prevention,
    buffer_containers=2, # Number of additional idle containers to maintain under active load.
    scaledown_window=30, # Max time (in seconds) a container can remain idle while scaling down.
    secrets=[modal.Secret.from_name("aws-secrets")]
)
@modal.asgi_app()
def unified_triton_server():
    print("🚀 Booting ONE Triton Instance inside ONE A100 Container...")
    
    # Spawns Triton in the background. It will automatically read 
    # your "aws-secrets" environment keys to mount s3://vkist-ml-model/
    cmd = ["tritonserver", "--model-repository=s3://vkist-ml-model/"]
    subprocess.Popen(cmd)
    
    print("📋 Triton background process delegated. Handing routing control over to FastAPI.")
    
    # Returns immediately! FastAPI now takes over the container lifecycle
    return web_app