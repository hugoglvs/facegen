import os
import csv
import torch
from torchvision import datasets, transforms
from diffusers import DiffusionPipeline,StableDiffusionPipeline
from dataclasses import dataclass

from deprecated import deprecated
import os
from .models import GeneratedImage, DreamboothModel
from django.conf import settings

class FaceGenPipeline:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(FaceGenPipeline, cls).__new__(cls)
        return cls._instance

    def __init__(self, model_id="runwayml/stable-diffusion-v1-5", seed=0):
        if not hasattr(self, '_initialized'):
            self.model_id = model_id
            self.device = self.__define_device()
            self.pipe = self.__load_pipeline()
            self.seed = seed
            self._initialized = True
            print(f"FaceGenPipeline initialized on {self.device} device")

    def __repr__(self):
        return f"FaceGenPipeline(model_id={self.model_id}, device={self.device})"
    
    def __call__(self, **kwargs):
        return self.pipe(**kwargs)
    
    def __define_device(self):
        if torch.cuda.is_available():
            return "cuda"
        if torch.backends.mps.is_available():
            return "mps"
        return "cpu"

    def __load_pipeline(self):
        pipe = StableDiffusionPipeline.from_pretrained(
            self.model_id,
            torch_dtype=torch.float,
            use_safetensors=True,
        )
        pipe.to(self.device)
        return pipe

@deprecated("Use FaceGenPipeline instead")
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

def random_token():
    import random
    import string
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))

def dreambooth_training(instance_data_dir, output_dir, unique_identifier, token):
    os.system('export MODEL_NAME="runwayml/stable-diffusion-v1-5')
    os.system(f'export INSTANCE_DIR="{instance_data_dir}"')
    os.system(f'export OUTPUT_DIR="{output_dir}/FaceGen_{token}"')
    os.system(f'accelerate launch train_dreambooth.py \
    --pretrained_model_name_or_path=$MODEL_NAME  \
    --instance_data_dir=$INSTANCE_DIR \
    --output_dir=$OUTPUT_DIR \
    --instance_prompt="A photo of {unique_identifier} man" \
    --gradient_checkpointing \
    --use_8bit_adam \
    --resolution=512 \
    --train_batch_size=1 \
    --gradient_accumulation_steps=1 \
    --learning_rate=5e-6 \
    --lr_scheduler="constant" \
    --lr_warmup_steps=0 \
    --max_train_steps=500 \
    ')