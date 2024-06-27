from django.urls import path
from . import views

urlpatterns = [
    # /home/
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('dreambooth/', views.dreambooth, name='dreambooth'),
    path('prompt/', views.prompt, name='prompt'),
    path('generate/', views.generate, name='generate'),
    path('webcam/', views.webcam, name='webcam'),
    path('start_dreambooth_training/', views.start_dreambooth_training, name='start_dreambooth_training'),
    path('upload_photos/', views.upload_photos, name='upload_photos'),
    path('delete_photo/', views.delete_photo, name='delete_photo'),
    path('history/', views.history, name='history'),
    path('info/<str:method>', views.info, name='info'),
    path('detail/<int:id>', views.details, name='details'),
]
