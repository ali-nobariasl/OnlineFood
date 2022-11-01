from verndor.models import Vender




def get_vendor(request):
    
    vendor = Vender.objects.get(user = request.user)
    return dict(vendor=vendor)