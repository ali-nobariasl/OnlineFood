from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db.models.fields.related import ForeignKey, OneToOneField
from django.db.models.signals import post_save , pre_save
from django.dispatch import receiver
from .models import User ,  UserProfile


@receiver(post_save, sender=User)
def post_save_create_profile(sender,instance,created,**kwargs):
    if created:
        UserProfile.objects.create(user=instance)
    else:
        try:
            profile = UserProfile.objects.create(user=instance)
            profile.save()
        except:
            UserProfile.objects.create(user=instance)
            
            
            
