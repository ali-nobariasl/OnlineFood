from django.urls import path

from .views import registerUser, registerVender


urlpatterns = [
    path('registerUser/',registerUser, name='registerUser'),
    path('registerVender/',registerVender, name='registerVender'),
]

