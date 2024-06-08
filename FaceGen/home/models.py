import datetime
from typing import overload

from django.db import models
from django.utils import timezone
from django.conf import settings

import os
import subprocess
import random
import string
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class GeneratedImage(models.Model):
    path = models.CharField(max_length=100, blank=True)
    date = models.DateTimeField(auto_now_add=True)
    prompt = models.CharField(max_length=256)
    negative_prompt = models.CharField(max_length=256)
    width = models.IntegerField()
    height = models.IntegerField()
    num_inference_steps = models.IntegerField()
    guidance_scale = models.FloatField()
    seed = models.IntegerField()

    def __str__(self):
        return f" {self.path} - {self.prompt} - {self.negative_prompt} - {self.width}x{self.height} - {self.num_inference_steps} steps - {self.guidance_scale} - {self.seed}"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if not self.path:
            self.path = f"{settings.MEDIA_URL}outputs/GeneratedImage_{self.id}.png"
            GeneratedImage.objects.filter(id=self.id).update(path=self.path)

    def get_filename(self):
        return self.path.split('/')[-1]

    def get_absolute_url(self):
        return os.path.abspath(self.path)

    def params(self):
        return {
            "prompt": self.prompt,
            "negative_prompt": self.negative_prompt,
            "width": int(self.width),
            "height": int(self.height),
            "num_inference_steps": int(self.num_inference_steps),
            "guidance_scale": int(self.guidance_scale),
            "seed": float(self.seed)
        }

    def was_generated_recently(self):
        return self.date >= timezone.now() - datetime.timedelta(days=1)

    @classmethod
    def history(cls, number):
        return cls.objects.order_by('-date')[:number]

class DreamboothModel(models.Model):
    token = models.CharField(max_length=6, unique=True, blank=True)
    identifier = models.CharField(max_length=100)
    training_steps = models.IntegerField()
    batch_size = models.IntegerField()
    path = models.CharField(max_length=255, blank=True)
    date = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.token:
            self.token = self.__create_token()
        super().save(*args, **kwargs)
        if not self.path:
            self.path = f"{settings.MEDIA_ROOT}dreambooth/FaceGen_{self.token}"
            DreamboothModel.objects.filter(id=self.id).update(path=self.path)

    def __str__(self):
        return f"{self.path}/{self.id}"

    def __create_token(self):
        token = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
        while DreamboothModel.objects.filter(token=token).exists():
            token = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
        return token

    def get_name(self):
        return self.path.split('/')[-1]

    def train(self, identifier="sks", training_steps=100, batch_size=1, model_name="runwayml/stable-diffusion-v1-5"):
        env = os.environ.copy()
        env["MODEL_NAME"] = model_name
        env["INSTANCE_DIR"] = os.path.join(settings.MEDIA_ROOT, 'users')
        if not self.path:
            self.path = os.path.join(settings.MEDIA_ROOT, f'dreambooth/FaceGen_{self.token}')
            DreamboothModel.objects.filter(id=self.id).update(path=self.path)
        env["OUTPUT_DIR"] = self.path

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
        except Exception as e:
            logger.exception("An error occurred while trying to run the training command.")
