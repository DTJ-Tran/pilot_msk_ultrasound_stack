#!/bin/bash

S3_BUCKET="s3://vkist-ml-model"

# Set the exact local baseline path where your updated config.pbtxt models reside
LOCAL_CONFIG_DIR="/Users/davestran/Downloads/vkist_internship/PILOT_PROJECT/workspace/sprint_1_2/codebase/infra/implementation/s3"

echo "📤 Syncing local config.pbtxt modifications up to S3 bucket repository..."

# Classification Configs
aws s3 cp "$LOCAL_CONFIG_DIR/angle_classify_convnext_tiny/config.pbtxt" "$S3_BUCKET/angle_classify_convnext_tiny/config.pbtxt"
aws s3 cp "$LOCAL_CONFIG_DIR/angle_classify_densenet/config.pbtxt" "$S3_BUCKET/angle_classify_densenet/config.pbtxt"
aws s3 cp "$LOCAL_CONFIG_DIR/angle_classify_efficientnet/config.pbtxt" "$S3_BUCKET/angle_classify_efficientnet/config.pbtxt"
aws s3 cp "$LOCAL_CONFIG_DIR/angle_classify_resnet50/config.pbtxt" "$S3_BUCKET/angle_classify_resnet50/config.pbtxt"
aws s3 cp "$LOCAL_CONFIG_DIR/angle_classify_swin_v2_s/config.pbtxt" "$S3_BUCKET/angle_classify_swin_v2_s/config.pbtxt"
aws s3 cp "$LOCAL_CONFIG_DIR/inflammation_model_efficientnet_b0_ultrasound_2_cls/config.pbtxt" "$S3_BUCKET/inflammation_model_efficientnet_b0_ultrasound_2_cls/config.pbtxt"

# Segmentation Configs
aws s3 cp "$LOCAL_CONFIG_DIR/segmentation_model_post_deeplabv3/config.pbtxt" "$S3_BUCKET/segmentation_model_post_deeplabv3/config.pbtxt"
aws s3 cp "$LOCAL_CONFIG_DIR/segmentation_model_post_deeplabv3_resnet101/config.pbtxt" "$S3_BUCKET/segmentation_model_post_deeplabv3_resnet101/config.pbtxt"
aws s3 cp "$LOCAL_CONFIG_DIR/segmentation_model_post_efficientfeedback/config.pbtxt" "$S3_BUCKET/segmentation_model_post_efficientfeedback/config.pbtxt"
aws s3 cp "$LOCAL_CONFIG_DIR/segmentation_model_unet3plus_att/config.pbtxt" "$S3_BUCKET/segmentation_model_unet3plus_att/config.pbtxt"
aws s3 cp "$LOCAL_CONFIG_DIR/segmentation_model_unet_resnet101/config.pbtxt" "$S3_BUCKET/segmentation_model_unet_resnet101/config.pbtxt"


# Ensemble Config 
aws s3 cp "$LOCAL_CONFIG_DIR/msk_vision_pipeline_ensemble/config.pbtxt" "$S3_BUCKET/msk_vision_pipeline_ensemble/config.pbtxt"

echo "✅ Configuration files successfully synced to S3 backend!"