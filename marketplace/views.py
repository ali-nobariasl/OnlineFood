from django.shortcuts import render, get_list_or_404

from vendor.models import Vendor


def marketplace(request):
    vendors = Vendor.objects.filter(is_approved=True, user__is_active=True)
    vendor_count = vendors.count()
    context = {
        'vendors': vendors,
        'vendor_count': vendor_count,
    }
    return render(request,'marketplace/listings.html', context)


def vendor_detail(request, vendor_slug):
    
    vendor = get_list_or_404(Vendor, vendor_slug=vendor_slug)
    context = {
        'vendor': vendor,
    }
    return render(request,'marketplace/vendor_detail.html', context)