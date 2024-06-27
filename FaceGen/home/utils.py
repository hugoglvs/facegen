from sympy import true
import torch
from torchvision import datasets, transforms
from diffusers import DiffusionPipeline,StableDiffusionPipeline

import datetime
import subprocess
import os
from .models import GeneratedImage
from django.conf import settings
from django.utils import timezone

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

    def __init__(self, model_id=settings.BASE_MODEL):
        if not hasattr(self, '_initialized'):
            self.model_id = model_id
            self.device = self.__define_device()
            self.pipe = self.__load_pipeline()
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
            #safety_checker=None,
            torch_dtype=torch.float,
            use_safetensors=True,
        )
        pipe.to(self.device)
        print(f"Pipeline loaded from {self.model_id}")
        self._initialized = True
        return pipe
    
    def __del__(self):
        self._initialized = False
        del self.pipe
    
    def is_base_model(self):
        return self.model_id == settings.BASE_MODEL

    def rebase(self):
        if self.model_id != settings.BASE_MODEL or not hasattr(self, 'pipe'):
            self.model_id = settings.BASE_MODEL
            self.__load_pipeline()

    
    def dreambooth(self, identifier="XYZ", training_steps=100, batch_size=1, base_model=settings.BASE_MODEL):
        try:
            del self.pipe
        except AttributeError:
            pass
        torch.cuda.empty_cache()
        print("Unloading pipeline")
        print("Starting Dreambooth training")
        env = os.environ.copy()
        env["MODEL_NAME"] = base_model
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
            print("Training command executed successfully.")
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

def remove_old_files(number_of_days):
    # Get all GeneratedImage objects older than `days` days
    old_images = GeneratedImage.objects.filter(date__lt=timezone.now() - datetime.timedelta(days=number_of_days))
    # Delete the files associated with these objects
    for image in old_images:
        try:
            os.remove(image.get_absolute_url())
            logger.info("File %s removed successfully", image.get_absolute_url())
        except Exception as e:
            logger.exception(f"An error occurred while trying to remove the file {image.get_absolute_url()}")
        image.delete()

def delete_not_saved_files():
    # Get all GeneratedImage objects that have not been saved
    saved_images = GeneratedImage.objects.all()
    # Delete all files from media/outputsnot that ain't in our database
    output_dir = os.path.join(settings.MEDIA_ROOT, 'outputs')
    for file in os.listdir(output_dir):
        if file not in [image.get_filename() for image in saved_images]:
            try:
                os.remove(os.path.join(output_dir, file))
                logger.info("File %s removed successfully", file)
            except Exception as e:
                logger.exception(f"An error occurred while trying to remove the file {file}")
    

