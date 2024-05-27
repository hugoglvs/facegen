from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
from .models import ImageOutput
from .utils import load_pipeline, generate_image

flag = False

# def view(request: HttpRequest) -> HttpResponse:

def index(request: HttpRequest) -> HttpResponse:
    return render(request, 
                  'home/index.html',
                  {
                      'history': ImageOutput.objects.all()[:5]
                  })

def generate(request: HttpRequest) -> HttpResponse:
    params = request.GET
    print(request.method, request.GET)
    return HttpResponse(params)
    return render(request, 
                  'home/generate.html',
                  {
                      'params': params
                  }
    )


# def generated_image(request: HttpRequest) -> HttpResponse:

if flag:
    pipe = load_pipeline()