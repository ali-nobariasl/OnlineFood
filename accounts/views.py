from django.shortcuts import render ,redirect
from django.http import HttpResponse
from django.contrib import messages
from .forms import UserForm
from .models import User
from django.utils import timezone
from verndor.forms import VendorForm


def registerUser(request):
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
    form = UserForm()
    v_form = VendorForm()
    context = {
        'form': form,
        'v_form': v_form,
    }
    return render(request, 'accounts/registerVender.html', context)

