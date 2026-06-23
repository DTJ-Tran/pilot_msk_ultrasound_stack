# Create folder

# aws s3api put-object --bucket vkist-ml-model --key angle_classify_densenet/
aws s3api put-object --bucket vkist-ml-model --key angle_classify_efficientnet/ # best_efficientnet_b2.pth
aws s3api put-object --bucket vkist-ml-model --key angle_classify_resnet50/ # best_resnet50.pth 
aws s3api put-object --bucket vkist-ml-model --key angle_classify_swin_v2_s/ # best_swin_v2_s.pth 
aws s3api put-object --bucket vkist-ml-model --key segmentation_model_post_deeplabv3_resnet101/ # best_model_deeplabv3_resnet101_seed_16.pth 
aws s3api put-object --bucket vkist-ml-model --key segmentation_model_post_deeplabv3/ # best_model_Deeplav3.pth 
aws s3api put-object --bucket vkist-ml-model --key segmentation_model_post_efficientfeedback/ # efficientfeedback.pth 
aws s3api put-object --bucket vkist-ml-model --key segmentation_model_unet_resnet101/ # unet_resnet101.pth
aws s3api put-object --bucket vkist-ml-model --key segmentation_model_unet3plus_att/ # unet3plus_att.pth 
aws s3api put-object --bucket vkist-ml-model --key inflammation_model_efficientnet_b0_ultrasound_2_cls/ # efficientnet_b0_ultrasound_2_class.pth 
aws s3api put-object --bucket vkist-ml-model --key msk_vision_pipeline_ensemble

# upload model
aws s3 mv s3://vkist-ml-model/best_densenet.pth s3://vkist-ml-model/angle_classify_densenet/best_densenet.pth
aws s3 mv s3://vkist-ml-model/best_efficientnet_b2.pth s3://vkist-ml-model/angle_classify_efficientnet/best_efficientnet_b2.pth
aws s3 mv s3://vkist-ml-model/best_model_deeplabv3_resnet101_seed_16.pth s3://vkist-ml-model/segmentation_model_post_deeplabv3_resnet101/best_model_deeplabv3_resnet101_seed_16.pth
aws s3 mv s3://vkist-ml-model/best_model_Deeplav3.pth s3://vkist-ml-model/segmentation_model_post_deeplabv3/best_model_Deeplav3.pth
aws s3 mv s3://vkist-ml-model/best_resnet50.pth s3://vkist-ml-model/angle_classify_resnet50/best_resnet50.pth
aws s3 mv s3://vkist-ml-model/best_swin_v2_s.pth s3://vkist-ml-model/angle_classify_swin_v2_s/best_swin_v2_s.pth
aws s3 mv s3://vkist-ml-model/efficientfeedback.pth s3://vkist-ml-model/segmentation_model_post_efficientfeedback/efficientfeedback.pth
aws s3 mv s3://vkist-ml-model/efficientnet_b0_ultrasound_2_class.pth s3://vkist-ml-model/inflammation_model_efficientnet_b0_ultrasound_2_cls/efficientnet_b0_ultrasound_2_class.pth
aws s3 mv s3://vkist-ml-model/unet_resnet101.pth s3://vkist-ml-model/segmentation_model_unet_resnet101/unet_resnet101.pth
aws s3 mv s3://vkist-ml-model/unet3plus_att.pth s3://vkist-ml-model/segmentation_model_unet3plus_att/unet3plus_att.pth
aws s3 mv s3://vkist-ml-model/best_convnext_tiny.pth s3://vkist-ml-model/angle_classify_convnext_tiny/best_convnext_tiny.pth



