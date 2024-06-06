import datetime
from typing import overload

from django.db import models
from django.utils import timezone
from django.conf import settings

# Create your models here.
# py manage.py makemigrations <appName> (creates a migration file)
# py manage.py sqlmigrate <appName> <numberMigration>  (returns the SQL code for the migration)
# py manage.py migrate <appName> (applies the migration)
    

# TO-DO: implement a manager for the GeneratedImage model
class GeneratedImage(models.Model):
    path = models.CharField(max_length=100)
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
        
        print("Absolute url", self.get_absolute_url())
        super().save(*args, **kwargs)

    def get_filename(self):
        return self.path.split('/')[-1]
    
    def get_absolute_url(self):
        path = self.path.replace(settings.MEDIA_URL, settings.MEDIA_ROOT)
        path = path.replace('/', '\\')
        return path
    
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

    token = models.CharField(max_length=8, unique=True)
    path = models.CharField(max_length=100)
    identifier = models.CharField(max_length=100)
    training_steps = models.IntegerField()
    batch_size = models.IntegerField()
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.path}/{self.id}"

    def __create_token(self):
        import random
        import string
        token = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
        if DreamboothModel.already_exists(token):
            return self.__create_token()
        return token
    
    def save(self, *args, **kwargs):
        self.token = self.__create_token()
        self.path = f"{settings.MEDIA_URL}dreambooth/FaceGen_{self.token}"
        super().save(*args, **kwargs)
    
    @classmethod
    def already_exists(cls, token):
        return cls.objects.filter(token=token).exists()