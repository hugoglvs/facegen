import os
import csv
import torch
from torchvision import datasets, transforms
from diffusers import DiffusionPipeline,StableDiffusionPipeline
from dataclasses import dataclass

import os
from .models import GeneratedImage
from django.conf import settings

def define_device():
    if torch.cuda.is_available():
        return "cuda"
    if torch.backends.mps.is_available():
        return "mps"
    return "cpu"

def load_pipeline():
    device = define_device()
    # generator = torch.Generator(device=device).manual_seed(42)
    model_id = "runwayml/stable-diffusion-v1-5"
    pipe = StableDiffusionPipeline.from_pretrained(
        model_id,
        torch_dtype=torch.float,
        use_safetensors=True,
    )
    pipe.to(device)
    return pipe

def generate_image(pipe: DiffusionPipeline, prompt: str, negative_prompt: str, width: int, height: int, num_inference_steps: int, guidance_scale: float, seed: int):
    params = {
        "prompt": prompt,
        "negative_prompt": negative_prompt,
        "width": width,
        "height": height,
        "num_inference_steps": num_inference_steps,
        "guidance_scale": guidance_scale,
        "seed": seed
    }
    result = pipe(**params)
    image = result.images[0]
    return image

def save_photo(photo_data, filename):
    file_path = os.path.join(settings.MEDIA_ROOT, "users", filename)
    print(file_path)
    with open(file_path, 'wb') as f:
        f.write(photo_data)
    return file_path
