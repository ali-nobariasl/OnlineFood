from django.shortcuts import render ,redirect
from django.http import HttpResponse
from django.contrib import messages , auth
from .forms import UserForm
from .models import User, UserProfile
from django.utils import timezone
from verndor.forms import VendorForm


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

def login(request):
    if request.user.is_authenticated:
        messages.warning(request, 'You are loged in already :D' )
        return redirect('dashboard')
    
    if request.method =="POST":
        email = request.POST['email']
        password = request.POST['password']
        
        user = auth.authenticate(email=email, password=password)
        if user is not None:
            auth.login(request, user)
            messages.success(request, 'you are now logged in')
            return redirect('dashboard')
        else:
            messages.error(request, 'invalid, you are not logged in')
            return redirect('login')
    return render(request, 'accounts/login.html')



def logout(request):
    auth.logout(request)
    messages.success(request, 'you are now logged out')
    return redirect('login')

def dashboard(request):
    return render(request, 'accounts/dashboard.html')

def myAccount(request):
    
    pass