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

def generate_image(pipe: DiffusionPipeline, prompt: str, negative_prompt: str, width: int, height: int, num_inference_steps: int, guidance_scale: float, seed: int = 0):
    params = {
        "prompt": prompt,
        "negative_prompt": negative_prompt,
        "width": width,
        "height": height,
        "num_inference_steps": num_inference_steps,
        "guidance_scale": guidance_scale,
        "seed": seed
    }
    print(params)
    result = pipe(**params)
    image = result.images[0]
    return image

def save_photo(photo_data, filename):
    file_path = os.path.join(settings.MEDIA_ROOT, "users", filename)
    print(file_path)
    with open(file_path, 'wb') as f:
        f.write(photo_data)
    return file_path

def dreambooth_training(instance_data_dir, output_dir, hey):
    os.system('export MODEL_NAME="runwayml/stable-diffusion-v1-5')
    os.system('export INSTANCE_DIR="./data"')
    os.system('export OUTPUT_DIR="models/facedell-model-amir"')
    os.system('accelerate launch train_dreambooth.py \
    --pretrained_model_name_or_path=$MODEL_NAME  \
    --instance_data_dir=$INSTANCE_DIR \
    --output_dir=$OUTPUT_DIR \
    --instance_prompt="a photo of sks man" \
    --gradient_checkpointing \
    --use_8bit_adam \
    --resolution=512 \
    --train_batch_size=1 \
    --gradient_accumulation_steps=1 \
    --learning_rate=5e-6 \
    --lr_scheduler="constant" \
    --lr_warmup_steps=0 \
    --max_train_steps=500 \
    # --validation_prompt="a photo of sks man" \
    # --num_validation_images=4 \
    # --validation_steps=100 \
    # --train_text_encoder \
    ')

def random_token():
    import random
    import string
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))

print(random_token())