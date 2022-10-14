from django.urls import path

from .views import registerUser, registerVender ,login,logout,dashboard,myAccount


urlpatterns = [
    path('registerUser/',registerUser, name='registerUser'),
    path('registerVender/',registerVender, name='registerVender'),
    
    path('login/', login, name='login'),
    path('logout/', logout, name='logout'),
    path('myAccount/', myAccount, name='myAccount'),
    path('dashboard/', dashboard, name='dashboard'),
    
]

