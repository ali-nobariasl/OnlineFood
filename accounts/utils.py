
def detectUser(user):
    if user.role==1:
        redirectUrl = 'vendorDashboard'
        return redirectUrl
    elif user.role == 2:
        redirectUrl = 'custDashboard'
        return redirectUrl
    elif user.role == None or user.is_superuser:
        redirectUrl = '/admin'
        return redirectUrl
    
    
    

def send_verification_email(request,user):
    pass