#!/bin/bash

# Define the absolute local path to your compiled TorchScript folder
LOCAL_DIR="PILOT_PROJECT/workspace/sprint_1_2/codebase/infra/implementation/MODEL_ZIP_PILOT_LT"
S3_BUCKET="s3://vkist-ml-model"

echo "📤 Starting upload workflow of LibTorch binaries to S3 bucket layout..."

# ==========================================
# 1. Classification Models
# ==========================================

echo "🔄 Uploading: Classification models..."
aws s3 cp "$LOCAL_DIR/best_densenet.pth" "$S3_BUCKET/angle_classify_densenet/1/model.pt"
aws s3 cp "$LOCAL_DIR/best_efficientnet_b2.pth" "$S3_BUCKET/angle_classify_efficientnet/1/model.pt"
aws s3 cp "$LOCAL_DIR/best_resnet50.pth" "$S3_BUCKET/angle_classify_resnet50/1/model.pt"
aws s3 cp "$LOCAL_DIR/best_swin_v2_s.pth" "$S3_BUCKET/angle_classify_swin_v2_s/1/model.pt"
aws s3 cp "$LOCAL_DIR/best_convnext_tiny.pth" "$S3_BUCKET/angle_classify_convnext_tiny/1/model.pt"
aws s3 cp "$LOCAL_DIR/efficientnet_b0_ultrasound_2_class.pth" "$S3_BUCKET/inflammation_model_efficientnet_b0_ultrasound_2_cls/1/model.pt"

# ==========================================
# 2. Segmentation Models
# ==========================================

echo "🔄 Uploading: Segmentation models..."
aws s3 cp "$LOCAL_DIR/best_model_deeplabv3_resnet101_seed_16.pth" "$S3_BUCKET/segmentation_model_post_deeplabv3_resnet101/1/model.pt"
aws s3 cp "$LOCAL_DIR/best_model_Deeplav3.pth" "$S3_BUCKET/segmentation_model_post_deeplabv3/1/model.pt"
aws s3 cp "$LOCAL_DIR/efficientfeedback.pth" "$S3_BUCKET/segmentation_model_post_efficientfeedback/1/model.pt"
aws s3 cp "$LOCAL_DIR/unet_resnet101.pth" "$S3_BUCKET/segmentation_model_unet_resnet101/1/model.pt"
aws s3 cp "$LOCAL_DIR/unet3plus_att.pth" "$S3_BUCKET/segmentation_model_unet3plus_att/1/model.pt"

echo "🎉 All local LibTorch models compiled down and synchronized with S3 Triton targets successfully!"