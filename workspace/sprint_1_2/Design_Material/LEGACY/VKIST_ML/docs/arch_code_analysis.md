# ML Model Architecture Report

| File | Architectures (code ranges) |
|------|-----------------------------|
| `ML/arch/unet3plus_att.py` | - **UNet3Plus_Attention** (87‑268)<br>  &nbsp;&nbsp;- SelfAttention (7‑25)<br>  &nbsp;&nbsp;- AttentionGate (28‑66)<br>  &nbsp;&nbsp;- conv_block (69‑83) |
| `ML/arch/efficientfeedback.py` | - **EfficientFeedbackNetwork** (171‑239)<br>  &nbsp;&nbsp;- convblock (9‑14)<br>  &nbsp;&nbsp;- DecoderBlock (17‑35)<br>  &nbsp;&nbsp;- ASPP_module (37‑66)<br>  &nbsp;&nbsp;- CAM_Module (68‑86)<br>  &nbsp;&nbsp;- S_Module (93‑131)<br>  &nbsp;&nbsp;- FeedbackSpatialAttention (134‑151)<br>  &nbsp;&nbsp;- StageAttentionwCAM (153‑168) |
| `ML/segment_anything/modeling/image_encoder.py` | - **ImageEncoderViT** (18‑119)<br>  &nbsp;&nbsp;- PatchEmbed (389‑420)<br>  &nbsp;&nbsp;- Block (122‑187)<br>  &nbsp;&nbsp;- Attention (190‑254) |
| `ML/segment_anything/modeling/prompt_encoder.py` | - **PromptEncoder** (17‑181)<br>  &nbsp;&nbsp;- PositionEmbeddingRandom (183‑226) |
| `ML/segment_anything/modeling/mask_decoder.py` | - **MaskDecoder** (17‑190)<br>  &nbsp;&nbsp;- MLP (168‑190) |
| `ML/segment_anything/modeling/transformer.py` | - **TwoWayTransformer** (17‑108)<br>  &nbsp;&nbsp;- TwoWayAttentionBlock (110‑183)<br>  &nbsp;&nbsp;- Attention (186‑243) |
| `ML/segment_anything/modeling/sam.py` | - **Sam** (19‑181) *(no internal sub‑architectures; uses imported modules)* |
