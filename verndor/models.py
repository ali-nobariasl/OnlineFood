from distutils.command import upload
from django.db import models
from accounts.models import User , UserProfile


class Vender(models.Model):
    user = models.OneToOneField(User, related_name="user", on_delete=models.CASCADE)
    user_profile= models.OneToOneField(UserProfile, related_name="user", on_delete=models.CASCADE)   
    vender_name = models.CharField(max_length=50)
    vender_license = models.ImageField(upload_to='vendor/license')
    is_approved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.vender_name
    
       