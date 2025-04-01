import torch
from diffusers import StableDiffusionInpaintPipeline
from PIL import Image

# Load Stable Diffusion inpainting model
pipe = StableDiffusionInpaintPipeline.from_pretrained(
  "runwayml/stable-diffusion-inpainting",
  torch_dtype=torch.float16
).to("cuda" if torch.cuda.is_available() else "cpu")

def change_outfit(image, mask, prompt="Change outfit to a saree"):
    resized_image = image.resize((512, 512))
    resized_mask = mask.resize((512, 512))

    result = pipe(prompt=prompt, image=resized_image, mask_image=resized_mask)
    return result.images[0]
