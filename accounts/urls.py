from django.urls import include, path

from . import views

urlpatterns = [
    path("", views.myAccount),
    path("registerUser/", views.registerUser, name="registerUser"),
    path("registerVendor/", views.registerVendor, name="registerVendor"),
    path("logout/", views.logout, name="logout"),
    path("login/", views.login, name="login"),
    path("myAccount/", views.myAccount, name="myAccount"),
    path("custdashboard/", views.custdashboard, name="custdashboard"),
    path("vendordashboard/", views.vendordashboard, name="vendordashboard"),
    path("activate/<uidb64>/<token>/", views.activate, name="activate"),
    path("forgot_password/", views.forgot_password, name="forgot_password"),
    path("reset_password_validate/<uidb64>/<token>/", views.reset_password_validate, name="reset_password_validate"),
    path("reset_password/", views.reset_password, name="reset_password"),
    path("vendor/", include("vendor.urls")),
]
