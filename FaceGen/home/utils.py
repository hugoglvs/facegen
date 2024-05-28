import os
import csv
import torch
from torchvision import datasets, transforms
from torch.utils.data import DataLoader
from torch.utils.data import Dataset
from transformers import CLIPTextModel, CLIPTokenizer
from diffusers import DiffusionPipeline,StableDiffusionPipeline, EulerDiscreteScheduler, UNet2DConditionModel, PNDMScheduler
from accelerate import Accelerator
from dataclasses import dataclass
from datasets import load_dataset

from .models import ImageInput, ImageOutput

def load_pipeline():
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    # generator = torch.Generator(device=device).manual_seed(42)
    model_id = "runwayml/stable-diffusion-v1-5"
    pipe = StableDiffusionPipeline.from_pretrained(
        model_id, 
        torch_dtype=torch.float,
        use_safetensors=True,
    )
    pipe.to(device)
    return pipe

def generate_image(pipe: DiffusionPipeline, image_input: ImageInput):
    print(image_input.params())
    result = pipe(**image_input.params())
    image = result.images[0]
    return image
    