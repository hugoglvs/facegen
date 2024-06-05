from django.urls import path
from . import views

urlpatterns = [
    # /home/
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('dreambooth/', views.dreambooth, name='dreambooth'),
    path('generate/', views.generate, name='generate'),
    path('webcam/', views.webcam, name='webcam'),
    path('upload_photos/', views.upload_photos, name='upload_photos'),
    path('delete_photo/', views.delete_photo, name='delete_photo'),
]
