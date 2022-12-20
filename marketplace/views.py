from django.shortcuts import render, get_object_or_404, HttpResponse 
from django.db.models import Prefetch
from django.http import JsonResponse

from vendor.models import Vendor
from menu.models import Category,FoodItem
from marketplace.models import Cart

def marketplace(request):
    vendors = Vendor.objects.filter(is_approved=True, user__is_active=True)
    vendor_count = vendors.count()
    context = {
        'vendors': vendors,
        'vendor_count': vendor_count,
    }
    return render(request,'marketplace/listings.html', context)


def vendor_detail(request, vendor_slug):
    
    vendor = get_object_or_404(Vendor, vendor_slug=vendor_slug)
    categories = Category.objects.filter(vendor=vendor).prefetch_related(
        Prefetch(
            'fooditems',
            queryset = FoodItem.objects.filter(is_available=True)
        )
    )
    context = {
        'vendor': vendor,
        'categories': categories,
    }
    return render(request,'marketplace/vendor_detail.html', context)


def add_to_cart(request, food_id=None):
    if request.user.is_authenticated():
        if request.is_ajax():
            try:
                footitem = FoodItem.objects.get(id=food_id)
                try:
                    chkCart = Cart.objects.get(user=request.user, fooditem=footitem)
                    chkCart.quantity += 1
                    chkCart.save()
                    return JsonResponse({
                    'status':'Success',
                    'message': 'Increased the cart quantity'})
                except:
                    chkCart = Cart.objects.create(user=request.user, fooditem=footitem, quantity=1)
                    return JsonResponse({
                    'status':'Success',
                    'message': 'Added to the food cart'}) 
            except:
                return JsonResponse({
                    'status':'failed',
                    'message': 'Invalid request'}) 
        else:
            return JsonResponse({
                'status':'failed',
                'message': 'Invalid request'})
    else:
        return JsonResponse({
            'status':'failed',
            'message': 'Please Login to continue'})