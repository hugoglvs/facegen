from django.urls import path
from . import views

urlpatterns = [
    # /home/
    path('', views.index, name='index'),
    path('generate/', views.generate, name='generate'),
    path('upload_photos/', views.upload_photos, name='upload_photos'),
]