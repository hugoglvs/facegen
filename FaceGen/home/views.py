from django.shortcuts import render
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import ImageOutput, ImageInput
from django.conf import settings
import os
import json
import base64

flag = True

# def view(request: HttpRequest) -> HttpResponse:

def index(request: HttpRequest) -> HttpResponse:
    return render(request, 
                  'home/index.html',
                  {
                      'history': ImageOutput.objects.all()[10:25]
                  })

@csrf_exempt
def generate(request: HttpRequest) -> HttpResponse:
    params = request.GET
    image_input = ImageInput(
        prompt=params['prompt'],
        negative_prompt=params['negative_prompt'],
        width=params['width'],
        height=params['height'],
        num_inference_steps=params['num_inference_steps'],
        guidance_scale=params['guidance_scale'],
        seed=0
    )
    image_input.save()
    filename = f"image_{image_input.id}.png"
    image = generate_image(pipe, image_input)
    image.save(f"{settings.MEDIA_ROOT}/{filename}")
    print(f"Image saved to {settings.MEDIA_ROOT}/{filename}")
    print(f"Image URL: {settings.MEDIA_URL}/{filename}")
    image_output = ImageOutput(path=f"{settings.MEDIA_URL}{filename}", params=image_input)
    image_output.save()

    context = {"image_output": image_output}
    return render(request, 'home/generate.html', context)

@csrf_exempt
def upload_photos(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        photos = data.get('photos', [])
        for idx, photo in enumerate(photos):
            photo_data = base64.b64decode(photo.split(',')[1])
            with open(f'media/photo_{idx}.png', 'wb') as f:
                f.write(photo_data)
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'failed'})

# def generated_image(request: HttpRequest) -> HttpResponse:

if flag:
    from .utils import load_pipeline, generate_image
    pipe = load_pipeline()