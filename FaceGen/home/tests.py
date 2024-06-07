from django.test import TestCase
from .models import GeneratedImage, DreamboothModel
from django.conf import settings

import datetime
from django.utils import timezone

# Create your tests here.
settings.AUTO_LOAD_PIPELINE = False
class GeneratedImageModelTests(TestCase):

    def setUp(self):
        GeneratedImage.objects.create(prompt="Test Prompt", negative_prompt="Test Negative Prompt", width=256, height=256, num_inference_steps=100, guidance_scale=0.1, seed=0).save()
        GeneratedImage.objects.create(prompt="Test Prompt 2", negative_prompt="Test Negative Prompt 2", width=512, height=512, num_inference_steps=200, guidance_scale=0.2, seed=1).save()
        GeneratedImage.objects.create(prompt="Test Prompt 3", negative_prompt="Test Negative Prompt 3", width=1024, height=1024, num_inference_steps=300, guidance_scale=0.3, seed=2).save()

    def test_instance_creation(self):
        """Test if the instance is created correctly"""
        image = GeneratedImage.objects.get(id=1)
        self.assertEqual(image.width, 256)
        self.assertEqual(image.height, 256)
        self.assertEqual(image.num_inference_steps, 100)
        self.assertEqual(image.guidance_scale, 0.1)
        self.assertEqual(image.seed, 0)
        self.assertEqual(image.path, f"{settings.MEDIA_URL}outputs/GeneratedImage_{image.id}.png", "Path is not correct")

    def test_was_generated_recently_with_future_image(self):
        # Maybe this shouldn't be allowed
        """was_generated_recently() returns True for images whose date is in the future."""
        time = timezone.now() + datetime.timedelta(days=30)
        future_image = GeneratedImage(date=time)
        self.assertIs(future_image.was_generated_recently(), True, "Future image was not generated recently !")

    def test_was_generated_recently_with_old_image(self):
        """was_generated_recently() returns False for images whose date is older than 1 day."""
        time = timezone.now() - datetime.timedelta(days=1, seconds=1)
        old_image = GeneratedImage(date=time)
        self.assertIs(old_image.was_generated_recently(), False, "Old image was generated recently !")

    def test_was_generated_recently_with_recent_image(self):
        """was_generated_recently() returns True for images whose date is within the last day."""
        time = timezone.now() - datetime.timedelta(hours=23, minutes=59, seconds=59)
        recent_image = GeneratedImage(date=time)
        self.assertIs(recent_image.was_generated_recently(), True, "Recent image was not generated recently !")

    def test_history(self):
        """history() returns the last 'number' images"""
        images = GeneratedImage.history(2)
        self.assertEqual(len(images), 2, "History does not return the correct number of images")
        self.assertEqual(images[0].id, 3, "History does not return the correct images")
        self.assertEqual(images[1].id, 2, "History does not return the correct images")
        self.assertNotEqual(images[0].id, 1, "History does not return the correct images")
        self.assertNotEqual(images[1].id, 1, "History does not return the correct images")


class DreamboothModelTests(TestCase):

    def setUp(self):
        DreamboothModel.objects.create(identifier="sks", training_steps=100, batch_size=1).save()
        DreamboothModel.objects.create(identifier="dlk", training_steps=200, batch_size=2).save()
        DreamboothModel.objects.create(identifier="axk", training_steps=300, batch_size=3).save()
    
    def test_instance_creation(self):
        """Test if the instance is created correctly"""
        model = DreamboothModelTests.objects.get(id=1)
        self.assertEqual(model.identifier, "sks")
        self.assertEqual(model.training_steps, 100)
        self.assertEqual(model.batch_size, 1)
        self.assertEqual(model.path, f"{settings.MEDIA_URL}dreambooth/FaceGen_{model.token}", "Path is not correct")
    
