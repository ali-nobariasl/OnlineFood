from verndor.models import Vender




def get_vendor(request):
    try:
        vendor = Vender.objects.get(user = request.user)
    except:
        vendor = None
    return dict(vendor=vendor)