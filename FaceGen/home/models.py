import datetime

from django.db import models
from django.utils import timezone

# Create your models here.
# py manage.py makemigrations <appName> (creates a migration file)
# py manage.py sqlmigrate <appName> <numberMigration>  (returns the SQL code for the migration)
# py manage.py migrate <appName> (applies the migration)

class ImageInput(models.Model):
    prompt = models.CharField(max_length=256)
    negative_prompt = models.CharField(max_length=256)
    width = models.IntegerField()
    height = models.IntegerField()
    num_inference_steps = models.IntegerField()
    guidance_scale = models.FloatField()
    seed = models.IntegerField()

    def __str__(self):
        return f"{self.prompt} - {self.negative_prompt} - {self.width}x{self.height} - {self.num_inference_steps} steps - {self.guidance_scale} - {self.seed}"

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

class ImageOutput(models.Model):
    path = models.CharField(max_length=100)
    date = models.DateTimeField(auto_now_add=True)
    params = models.ForeignKey('home.ImageInput', on_delete=models.CASCADE)

    def __str__(self):
        return self.path
    
    def was_generated_recently(self):
        return self.date >= timezone.now() - datetime.timedelta(days=1)
