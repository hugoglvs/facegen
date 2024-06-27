from django.shortcuts import render
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .utils import FaceGenPipeline, save_photo, remove_old_files, delete_not_saved_files
from .models import GeneratedImage
from django.conf import settings
from django.core.files.base import ContentFile
import os
import logging
import base64


logger = logging.getLogger(__name__)

if settings.AUTO_LOAD_PIPELINE:
    pipe = FaceGenPipeline()

# def view(request: HttpRequest) -> HttpResponse:

# Pages to render

def index(request: HttpRequest) -> HttpResponse:
    delete_not_saved_files()
    remove_old_files(15)
    pipe.rebase()
    return render(request,'home/index.html')

def dreambooth(request: HttpRequest) -> HttpResponse:
    return render(request, 'home/dreambooth.html')

def about(request: HttpRequest) -> HttpResponse:
    return render(request, 'home/about.html')

#

@csrf_exempt
def generate(request: HttpRequest) -> HttpResponse:
    params = request.GET.dict()
    generated_image = GeneratedImage.objects.create(**params)
    if not pipe.is_base_model():
        generated_image.dreambooth = True
    print(generated_image)
    image = pipe(**generated_image.params()).images[0]
    image.save(os.path.join(settings.MEDIA_ROOT, "outputs", generated_image.get_filename()), "PNG")
    generated_image.save()
    context = {"image_output": generated_image}
    return render(request, 'home/components/image_output.html', context)

# Components

@csrf_exempt
def prompt(request: HttpRequest) -> HttpResponse:
    return render(request, 'home/components/prompt.html')

@csrf_exempt
def webcam(request: HttpRequest) -> HttpResponse:
    return render(request, 'home/components/webcam.html')

@csrf_exempt
def history(request: HttpRequest) -> HttpResponse:
    return render(request, 'home/components/history.html',
                  {'history': GeneratedImage.history(10)} 
                  )

@csrf_exempt
def info(request: HttpRequest, method: str) -> HttpResponse:
    context = {"method": method}  # can be "dreambooth" or "stable_diffusion"
    return render(request, 'home/components/info.html', context)

@csrf_exempt
def details(request: HttpRequest, id: int) -> HttpResponse:
    context = {"image": GeneratedImage.objects.get(id=id)}
    return render(request, 'home/components/details.html', context)

# Actions

@csrf_exempt
def start_dreambooth_training(request: HttpRequest) -> JsonResponse:
    # Upload "user_photos" to "users" folder by running "upload_photos" view
    upload_photos(request)
    print("Photos uploaded")
    pipe.dreambooth()
    return render(request, 'home/components/prompt.html', {"dreambooth": True})

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
