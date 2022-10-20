from base64 import urlsafe_b64decode
from django.shortcuts import render ,redirect
from django.http import HttpResponse
from django.contrib import messages , auth
from .forms import UserForm
from .models import User, UserProfile
from django.utils import timezone
from verndor.forms import VendorForm
from accounts.utils import detectUser , send_verification_email , send_password_resert_email
from django.contrib.auth.decorators import login_required , user_passes_test
from django.core.exceptions import PermissionDenied 
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator


# Restrict the vendor from accessing the customer page
def check_role_vendor(user):
    if user.role == 1:
        return True
    else:
        raise PermissionDenied

# Restrict the customer from accessing the vendor page
def check_role_customer(user):
    if user.role == 2:
        return True
    else:
        raise PermissionDenied


def registerUser(request):
    if request.user.is_authenticated:
        messages.warning(request, 'You are loged in already :D' )
        return redirect('dashboard')
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            password = form.cleaned_data['password']
            user =form.save(commit=False)
            user.set_password(password)
            user.role = User.CUSTOMER
            user.save()
            # Send verification email
            send_verification_email(request, user)
            messages.success(request, 'your account has been registered successfully')
            return redirect('registerUser')
    else:
        form = UserForm()
    context = {
        'form': form,
    }
    return render(request, 'accounts/registerUser.html', context)

def registerVender(request):
    if request.user.is_authenticated:
        messages.warning(request, 'You are loged in already :D' )
        return redirect('dashboard')
    if request.method == 'POST':
        form = UserForm(request.POST)
        v_form = VendorForm(request.POST, request.FILES)
        if form.is_valid() and v_form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = User.objects.create_user(username=username, email=email, password=password,first_name=first_name, last_name=last_name)
            user.role = User.VENDOR
            user.save()
            user_profile = UserProfile.objects.get(user= user)
            vendor = v_form.save(commit=False)
            vendor.user = user
            vendor.user_profile = user_profile
            vendor.save()
            # Send verification email
            send_verification_email(request, user)
            messages.success(request,'your account has been successfully registered. please wait for approval.')
        else:
            print(form.errors)
    else:
        v_form = VendorForm()
        form = UserForm()
    context = {
        'form': form,
        'v_form': v_form,
    }
    
    return render(request, 'accounts/registerVender.html', context)

def activate(request,uidb64, token):
    # Active the user by setting the is_active status to True
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User._default_manager.get(pk=uid)  
    except(TypeError,ValueError,OverflowError,User.DoesNotExist):
        user = None
    if user is None and default_token_generator.check_token(user,token):
        user.is_active = True   
        user.save()
        messages.success(request,'Con...! your account has been activated')
        return redirect('myAccount')
    else:
        messages.error(request,'invalid activation link !!!')  
        return redirect('myAccount')
    
def login(request):
    if request.user.is_authenticated:
        messages.warning(request, 'You are loged in already :D' )
        return redirect('myAccount')
    
    if request.method =="POST":
        email = request.POST['email']
        password = request.POST['password']
        
        user = auth.authenticate(email=email, password=password)
        if user is not None:
            auth.login(request, user)
            messages.success(request, 'you are now logged in')
            return redirect('myAccount')
        else:
            messages.error(request, 'invalid, you are not logged in')
            return redirect('login')
    return render(request, 'accounts/login.html')

def logout(request):
    auth.logout(request)
    messages.success(request, 'you are now logged out')
    return redirect('login')



@login_required(login_url='login')
@user_passes_test(check_role_customer)
def custDashboard(request):
    return render(request, 'accounts/custdashboard.html')



@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def vendorDashboard(request):
    return render(request, 'accounts/vendordashboard.html')



@login_required(login_url='login')
def myAccount(request):
    user = request.user
    redirectUrl = detectUser(user)
    return redirect(redirectUrl)


def forget_password(request):
    if request.user == 'POST':
        email = request.POST['email']
        if User.objects.filter(email=email).filter():
            user = User.objects.get(email__exact=email)
            
            # send reset password email
            send_password_resert_email(request, user)
            messages.success(request,'password reset link has been sent to your mail address. ')
            return redirect('login')
        else:
            messages.success(request,'account does not exist')
            return redirect('forget_password')
        
    return render(request,'accounts/forget_password.html')



def reset_password_validate(request,uidb64, token):
    return

def reset_password(request):
    return  render(request, 'accounts/reset_password.html') 