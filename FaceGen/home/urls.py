from django.urls import path
from . import views

urlpatterns = [
    # /home/
    path('', views.index, name='index'),
    path('generate/', views.generate, name='generate')
    # /home/card/
    # path('card/', views.card, name='card')
]