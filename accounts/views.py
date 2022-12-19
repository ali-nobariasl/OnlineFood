from django.shortcuts import render , redirect
from django.contrib import messages , auth
from django.contrib.auth.decorators import login_required , user_passes_test
from django.core.exceptions import PermissionDenied
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator
from django.template.defaultfilters import slugify


from .utils import detectUser , send_verification_email 
from .forms import UserForm 
from .models import User , UserProfile
from vendor.models import Vendor
from vendor.forms import  VendorForm


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
        messages.warning(request, 'you are already logged in')
        return redirect('myAccount')
    
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            #  Creating user by using FORM
            #password = form.cleaned_data['password']
            #user = form.save(commit=False)
            #user.set_password(password)
            #user.role = User.CUSTOMER
            #user.save()
            
            # Creating user by using Function
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = User.objects.create(username=username, email=email,first_name=first_name,last_name=last_name, password=password)
            user.role = User.CUSTOMER
            user.save()
                        
            # Send Verification mail 
            mail_subject = "Please active your account :D "
            mail_template = 'accounts/emails/account_verification_email.html'
            send_verification_email(request, user,mail_subject, mail_template)

            messages.success(request, 'your account has been created successfully')
            return redirect('registerUser')
        else:
            print('invalid')
            print(form.errors)
    else:
        form = UserForm()
    context = {
        'form': form,
    }
    return render(request, 'accounts/registerUser.html', context)


def registerVendor(request):
    if request.user.is_authenticated:
        messages.warning(request, 'you are already logged in')
        return redirect('myAccount')
    elif request.method == 'POST':
        form = UserForm(request.POST)
        v_form = VendorForm(request.POST, request.FILES)
        
        if form.is_valid() and v_form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = User.objects.create(username=username, email=email,first_name=first_name,last_name=last_name, password=password)
            user.role = User.VENDOR
            user.save()
            vendor = v_form.save(commit=False)
            vendor.user = user
            vendor_name = v_form.cleaned_data['vendor_name']
            vendor.vendor_slug = slugify(vendor_name)+ '-'+ str(user.id)
            user_profile = UserProfile.objects.get(user=user)
            vendor.user_profile = user_profile
            vendor.save()
            
            # Send Verification mail 
            mail_subject = "Please active your account :D "
            mail_template = 'accounts/emails/account_verification_email.html'
            send_verification_email(request, user,mail_subject, mail_template)
            
            messages.success(request, 'your account has been created successfully')
            return redirect('registerVendor')
        else:
            print('invalid form')
            print(form.errors)
    else:
        form = UserForm()
        v_form = VendorForm()
    
    context = {
        'form': form,
        'v_form': v_form,
    }
    return render(request, 'accounts/registerVendor.html', context)


def activate(request,uidb64, token):
    # Activate the user by setting the is_active status to True
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, 'Congratulation! Your account is activated.')
        return redirect('myAccount')
    else:
        messages.error(request, 'Invalid activation link')
        return redirect('myAccount')
    
def login(request):
    if request.user.is_authenticated:
        messages.warning(request, 'you are already logged in')
        return redirect('myAccount')
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        print('.......................')
        print(password)
        user = auth.authenticate(email=email, password=password)
        if user is not None:
            auth.login(request, user)
            messages.success(request, 'your are logged in successfully')
            return redirect('myAccount')
        else:
            messages.error(request, 'your username or password is incorrect')
            return redirect('login')
    return render (request, 'accounts/login.html')


def logout(request):
    auth.logout(request)
    messages.info(request, 'you are not logged out successfully')
    return redirect('login')



@login_required(login_url='login')
@user_passes_test(check_role_customer)
def custdashboard(request):
    return render (request, 'accounts/custdashboard.html')


@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def vendordashboard(request):
    return render (request, 'accounts/vendordashboard.html')



@login_required(login_url='login')
def myAccount(request):
    user = request.user
    redirectUrl = detectUser(user)
    return redirect(redirectUrl)



def forgot_password(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        user = User.objects.get(email__exact=email)
        if user is not None:
            # send reset password email
            mail_subject = "Reset Your Password :>"
            mail_template = 'accounts/emails/reset_password_email.html'
            send_verification_email(request, user,mail_subject, mail_template)
            messages.success(request, 'password reset email sent successfully')
            return redirect('login')
        else:
            messages.error(request, 'account is not exist')
            return redirect('forgot_password')    
    return render (request, 'accounts/forgot_password.html')



def reset_password_validate(request,uidb64, token):
    # validating the user
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        
        request.session['uid'] = uid
        messages.success(request, 'please reset your password')
        return redirect('reset_password')
    else:
        messages.error(request, 'The link is expired. You Cant make fun of me ')
        return redirect('myAccount')



def reset_password(request):
    if request.method == 'POST':
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        if confirm_password == password :
            pk = request.session.get('uid')
            user = User.objects.get(pk = pk)
            user.set_password(password)
            user.is_active = True
            user.save()
            messages.success(request, 'Password changed successfully')
            return redirect('login')
            
        else:
            messages(request, 'Passwords are not match. ')
            return redirect('reset_password')
        
    return render (request, 'accounts/reset_password.html')