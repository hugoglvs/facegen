from django.contrib import admin
from .models import ImageInput, ImageOutput

# Register your models here. (This is where you can add models to the admin page so you can view/edit them)
admin.site.register(ImageInput)
admin.site.register(ImageOutput)