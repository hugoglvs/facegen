from django.shortcuts import render
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .utils import save_photo
from .models import GeneratedImage
from django.conf import settings
from django.core.files.base import ContentFile
import os
import json
import base64

flag = False

# def view(request: HttpRequest) -> HttpResponse:

def index(request: HttpRequest) -> HttpResponse:
    return render(request,
                  'home/index.html',
                  {
                      'history': GeneratedImage.objects.all()[10:25]
                  })

def about(request: HttpRequest) -> HttpResponse:
    return render(request, 'home/about.html')

@csrf_exempt
def generate(request: HttpRequest) -> HttpResponse:
    # if not already loaded, load the pipeline
    params = request.GET.dict()
    print("Bonjour", params)
    generated_image = GeneratedImage.objects.create(**params)
    print(generated_image)
    generated_image.save()
    image = generate_image(pipe, **generated_image.params())
    print(f"A sauvegarder : {settings.MEDIA_ROOT}{generated_image.filename()}")
    image.save(f"{settings.MEDIA_ROOT}/{generated_image.filename()}")
    print(f"Image saved to {generated_image.path}")
    context = {"image_output": generated_image}
    return render(request, 'home/components/image_output.html', context)

@csrf_exempt
def webcam(request: HttpRequest) -> HttpResponse:
    return render(request, 'home/components/webcam.html')

@csrf_exempt
def upload_photos(request):
    if request.method == "POST":
        photos = request.POST.getlist("user_photos")
        saved_photos = []
        for index, photo in enumerate(photos):
            if photo:
                photo_data = base64.b64decode(photo.split(",")[1])
                saved_photo_path = save_photo(photo_data, f"photo_{index}.png")
                saved_photos.append(saved_photo_path)
        return JsonResponse({"status": "success", "photos": saved_photos})
    return JsonResponse({"status": "failure"}, status=400)

if flag:
    from .utils import load_pipeline, generate_image
    pipe = load_pipeline()
