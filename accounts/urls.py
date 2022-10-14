from django.urls import path

from .views import registerUser, registerVender ,login,logout,custDashboard,myAccount ,vendorDashboard


urlpatterns = [
    path('registerUser/',registerUser, name='registerUser'),
    path('registerVender/',registerVender, name='registerVender'),
    
    path('login/', login, name='login'),
    path('logout/', logout, name='logout'),
    path('myAccount/', myAccount, name='myAccount'),
    path('custDashboard/', custDashboard, name='custDashboard'),
    path('vendorDashboard/', vendorDashboard, name='vendorDashboard'),
    
    
]

