import os
import csv
import torch
from torchvision import datasets, transforms
from diffusers import DiffusionPipeline,StableDiffusionPipeline
from dataclasses import dataclass

import subprocess
import os
from .models import GeneratedImage
from django.conf import settings

import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class FaceGenPipeline:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(FaceGenPipeline, cls).__new__(cls)
        return cls._instance

    def __init__(self, model_id="runwayml/stable-diffusion-v1-5"):
        if not hasattr(self, '_initialized'):
            self.model_id = model_id
            self.device = self.__define_device()
            self.pipe = self.__load_pipeline()
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
            safety_checker=None,
            torch_dtype=torch.float,
            use_safetensors=True,
        )
        pipe.to(self.device)
        return pipe
    
    def __del__(self):
        del self.pipe
    
    def get_model_id(self):
        return self.model_id

    def is_runway(self):
        return self.model_id == "runwayML/stable-diffusion-v1-5"
    
    def dreambooth(self, identifier="sks", training_steps=100, batch_size=1, model_name="runwayml/stable-diffusion-v1-5"):
        del self.pipe
        print("Heeey")
        env = os.environ.copy()
        env["MODEL_NAME"] = model_name
        env["INSTANCE_DIR"] = os.path.join(settings.MEDIA_ROOT, 'users')
        dreambooth_path = os.path.join(settings.MEDIA_ROOT, 'FaceGen/stable-diffusion-dreambooth')
        env["OUTPUT_DIR"] = dreambooth_path

        # Ensure the output directory exists and is writable
        if not os.path.exists(env["OUTPUT_DIR"]):
            os.makedirs(env["OUTPUT_DIR"], exist_ok=True)

        logger.info(f"Training output directory: {env['OUTPUT_DIR']}")

        script_path = os.path.join(settings.BASE_DIR, 'home', 'static', 'home', 'train_dreambooth.py')

        command = [
            "accelerate", "launch", script_path,
            "--pretrained_model_name_or_path", env["MODEL_NAME"],
            "--instance_data_dir", env["INSTANCE_DIR"],
            "--output_dir", env["OUTPUT_DIR"],
            "--instance_prompt", f"A photo of {identifier} man",
            "--gradient_checkpointing",
            "--use_8bit_adam",
            "--resolution=512",
            f"--train_batch_size={batch_size}",
            "--gradient_accumulation_steps=1",
            "--learning_rate=5e-6",
            "--lr_scheduler=constant",
            "--lr_warmup_steps=0",
            f"--max_train_steps={training_steps}"
        ]

        try:
            result = subprocess.run(command, env=env, capture_output=True, text=True)
            logger.info("Command output: %s", result.stdout)
            logger.error("Command error output: %s", result.stderr)
            self.model_id = dreambooth_path
            self.pipe = self.__load_pipeline()
            
        except Exception as e:
            logger.exception("An error occurred while trying to run the training command.")

        


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
