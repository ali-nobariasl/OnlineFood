from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import get_object_or_404, redirect, render
from django.template.defaultfilters import slugify

from accounts.forms import UserProfileForm
from accounts.models import UserProfile
from accounts.views import check_role_vendor
from menu.forms import CategoryForm, FoodItemForm
from menu.models import Category, FoodItem

from .forms import VendorForm
from .models import Vendor


def get_vendor(request):
    vendor = Vendor.objects.get(user=request.user)
    return vendor


@login_required(login_url="login")
@user_passes_test(check_role_vendor)
def vprofile(request):
    profile = get_object_or_404(UserProfile, user=request.user)
    vendor = get_object_or_404(Vendor, user=request.user)

    if request.method == "POST":
        profile_form = UserProfileForm(request.POST, request.FILES, instance=profile)
        vendor_form = VendorForm(request.POST, request.FILES, instance=vendor)

        if profile_form.is_valid() and vendor_form.is_valid():
            profile_form.save()
            vendor_form.save()
            messages.success(request, "settings updated successfully")
            return redirect("vprofile")
        else:
            print(profile_form.errors)
            print(vendor_form.errors)
    else:
        profile_form = UserProfileForm(instance=profile)
        vendor_form = VendorForm(instance=vendor)

    context = {
        "profile_form": profile_form,
        "vendor_form": vendor_form,
        "profile": profile,
        "vendor": vendor,
    }
    return render(request, "vendor/vprofile.html", context)


@login_required(login_url="login")
@user_passes_test(check_role_vendor)
def menu_builder(request):
    vendor = get_vendor(request)
    categories = Category.objects.filter(vendor=vendor).order_by("created_at")
    context = {
        "vendor": vendor,
        "categories": categories,
    }
    print(categories)
    return render(request, "vendor/menu_builder.html", context)


@login_required(login_url="login")
@user_passes_test(check_role_vendor)
def fooditems_by_category(request, pk=None):
    vendor = get_vendor(request)
    category = get_object_or_404(Category, pk=pk)
    fooditems = FoodItem.objects.filter(category=category, vendor=vendor)

    context = {
        "fooditems": fooditems,
        "category": category,
    }
    return render(request, "vendor/fooditems_by_category.html", context)


def add_category(request):
    if request.method == "POST":
        form = CategoryForm(request.POST)
        if form.is_valid():
            category_name = form.cleaned_data["category_name"]
            category = form.save(commit=False)
            category.sluge = slugify(category_name)
            category.vendor = get_vendor(request)
            form.save()
            messages.success(request, "your category added successfully")
            return redirect("menu_builder")
        else:
            print(form.errors)
    else:
        form = CategoryForm()
    context = {
        "form": form,
    }
    return render(request, "vendor/add_category.html", context)


def edit_category(request, pk=None):
    category = get_object_or_404(Category, pk=pk)

    if request.method == "POST":
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            category_name = form.cleaned_data["category_name"]
            category = form.save(commit=False)
            
            category.vendor = get_vendor(request)
            category.save()
            category.sluge = slugify(category_name)+ '-'+ str(category.id)
            category.save()
            messages.success(request, "Updated successfully")
            redirect("menu_builder")
        else:
            print(form.errors)
    else:
        form = CategoryForm(instance=category)

    context = {
        "form": form,
        "category": category,
    }
    return render(request, "vendor/edit_category.html", context)


def delete_category(request, pk=None):
    category = Category.objects.get(pk=pk)
    category.delete()
    messages.success(request, "Delete successfully")
    return redirect("menu_builder")


def add_food(request):
    if request.method == "POST":
        form = FoodItemForm(request.POST, request.FILES)
        if form.is_valid():
            food_title = form.cleaned_data["food_title"]
            food = form.save(commit=False)
            food.vendor = get_vendor(request)
            food.sluge = slugify(food_title)
            form.save()
            messages.success(request, "Food item added successfully")
            return redirect("fooditems_by_category", food.category.id)
        else:
            print(form.errors)
    else:
        form = FoodItemForm()
        form.fiels["category"] = food.category.filter(vendor=get_vendor(request))
    context = {
        "form": form,
    }
    return render(request, "vendor/add_food.html", context)


def edit_food(request, pk=None):
    fooditem = FoodItem.objects.get(pk=pk)
    if request.method == "POST":
        form = FoodItemForm(request.POST, request.FILES, instance=fooditem)
        if form.is_valid():
            food_title = form.cleaned_data["food_title"]
            food = form.save(commit=False)
            food.vendor = get_vendor(request)
            food.sluge = slugify(food_title)
            food.save()
            messages.success(request, "Food item updated successfully")
            redirect("menu_builder")
        else:
            print(form.errors)
    else:

        form = FoodItemForm(instance=fooditem)
        form.fiels["category"] = food.category.filter(vendor=get_vendor(request))

    context = {
        "form": form,
        "food": fooditem,
    }
    return render(request, "vendor/edit_food.html", context)


def delete_food(request, pk):
    fooditem = FoodItem.objects.get(pk=pk)
    fooditem.delete()
    messages.success(request, "Delete successfully")
    return redirect("menu_builder")
