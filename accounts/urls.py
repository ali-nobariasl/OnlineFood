from django.urls import path , include

from .views import registerUser, registerVender ,login,logout,custDashboard,myAccount ,vendorDashboard , activate,reset_password_validate,forget_password,reset_password ,myAccount


urlpatterns = [
    path('', myAccount),
    path('registerUser/',registerUser, name='registerUser'),
    path('registerVender/',registerVender, name='registerVender'),
    
    path('login/', login, name='login'),
    path('logout/', logout, name='logout'),
    path('myAccount/', myAccount, name='myAccount'),
    path('custDashboard/', custDashboard, name='custDashboard'),
    path('vendorDashboard/', vendorDashboard, name='vendorDashboard'),
    
    path('activate/<uidb64>/<token>/', activate, name='activate'),
    
    path ('forget_password/', forget_password, name='forget_password'),
    path ('reset_password_validate/<uidb64>/<token>', reset_password_validate, name='reset_password_validate'),
    path ('reset_password/', reset_password, name='reset_password'),
    
    
    path('vendor/', include('verndor.urls'))
]

