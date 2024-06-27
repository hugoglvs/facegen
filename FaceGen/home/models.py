import datetime
from typing import overload

from django.db import models
from django.utils import timezone
from django.conf import settings

import os
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class GeneratedImage(models.Model):
    path = models.CharField(max_length=100, blank=True)
    date = models.DateTimeField(auto_now_add=True)
    prompt = models.CharField(max_length=256)
    negative_prompt = models.CharField(max_length=256)
    num_inference_steps = models.IntegerField()
    guidance_scale = models.FloatField()
    dreambooth = models.BooleanField(default=False)

    def __str__(self):
        return f" {self.path} - {self.prompt} - {self.negative_prompt} - {self.num_inference_steps} steps - {self.guidance_scale}"

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
            "num_inference_steps": int(self.num_inference_steps),
            "guidance_scale": int(self.guidance_scale),
        }

    def was_generated_recently(self):
        return self.date >= timezone.now() - datetime.timedelta(days=1)

    @classmethod
    def history(cls, number):
        return cls.objects.filter(dreambooth=False).order_by('-date')[:number]
