from django.shortcuts import render
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .utils import FaceGenPipeline, generate_image, save_photo
from .models import GeneratedImage, DreamboothModel
from django.conf import settings
from django.core.files.base import ContentFile
import os
import json
import base64

# def view(request: HttpRequest) -> HttpResponse:

# Pages to render

def index(request: HttpRequest) -> HttpResponse:
    return render(request,'home/index.html',
                  {'history': GeneratedImage.history(10)}
                  )

def dreambooth(request: HttpRequest) -> HttpResponse:
    return render(request, 'home/dreambooth.html')

def about(request: HttpRequest) -> HttpResponse:
    context = { "gradient-type": "circular"}
    return render(request, 'home/about.html', context)

# 

@csrf_exempt
def generate(request: HttpRequest) -> HttpResponse:
    params = request.GET.dict()
    generated_image = GeneratedImage.objects.create(**params)
    generated_image.save()
    print(generated_image)
    image = pipe(**generated_image.params()).images[0]
    image.save(f"{settings.MEDIA_ROOT}\outputs\{generated_image.get_filename()}")
    context = {"image_output": generated_image,
               'history': GeneratedImage.history(10)
               }
    return render(request, 'home/components/image_output.html', context)

# Components

@csrf_exempt
def webcam(request: HttpRequest) -> HttpResponse:
    return render(request, 'home/components/webcam.html')

# Actions

@csrf_exempt
def start_dreambooth_training(request: HttpRequest) -> JsonResponse:
    # Upload "user_photos" to "users" folder by running "upload_photos" view
    upload_photos(request)
    print("Photos uploaded")
    # Create DreamboothModel instance with the uploaded photos
    params = request.POST.dict().copy()
    del params["user_photos"]
    print(params)
    dreambooth_model = DreamboothModel(**params)
    dreambooth_model.train(**params)
    dreambooth_model.save()
    return JsonResponse({"status": "success"})

@csrf_exempt
def upload_photos(request: HttpRequest) -> JsonResponse:
    if request.method == "POST":
        photos = request.POST.getlist("user_photos")
        saved_photos = []
        for index, photo in enumerate(photos):
            if photo:
                photo_data = base64.b64decode(photo.split(",")[1])
                saved_photo_path = save_photo(photo_data, f"photo_{index}.png")
                saved_photos.append(saved_photo_path)
                print(f"Saved photo {index}")
        return JsonResponse({"status": "success", "photos": saved_photos })
    return JsonResponse({"status": "failure"}, status=400)

@csrf_exempt
def delete_photo(request: HttpRequest) -> JsonResponse:
    if request.method == "POST":
        data = request.POST.dict()
        print(data)
        photo = GeneratedImage.objects.get(id=data["id"])
        try:
            os.remove(f"{settings.BASE_DIR}/{photo.path}")
        except FileNotFoundError:
            print("File not found")
        photo.delete()
        return JsonResponse({"status": "success"})
    return JsonResponse({"status": "failure"}, status=400)

if settings.AUTO_LOAD_PIPELINE:
    pipe = FaceGenPipeline()
