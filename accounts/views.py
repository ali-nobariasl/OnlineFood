from django.shortcuts import render ,redirect
from django.http import HttpResponse
from .forms import UserForm
from .models import User

def registerUser(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            password = form.cleaned_data['password']
            user =form.save(commit=False)
            user.set_password(password)
            user.role = User.CUSTOMER
            user.save()
            return redirect('registerUser')
    else:
        form = UserForm()
    context = {
        'form': form,
    }
    return render(request, 'accounts/registerUser.html', context)