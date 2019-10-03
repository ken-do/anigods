from django.db import models
from django.contrib.auth.models import AbstractUser,UserManager

# Create your models here.

class CustomUserManager(UserManager):
    pass


def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return 'users/user_{0}/{1}'.format(instance.id, filename)

class CustomUser(AbstractUser):
    objects = CustomUserManager()
    display_name = models.CharField(verbose_name='display_name', max_length=255, blank=True, null=True)
    bio = models.CharField(verbose_name='intro', max_length=255, default="")
    avatar = models.ImageField(upload_to=user_directory_path, null=True, blank=True)
    name_last_updated_at = models.DateField(auto_now=False, auto_now_add=False,blank=True,null=True)
