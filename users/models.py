from django.db import models
from django.contrib.auth.models import AbstractUser
from cloudinary.models import CloudinaryField

# Create your models here.
class CustomUser(AbstractUser):
    # profile_image = models.ImageField(upload_to='profile_images', blank=True, default='profile_images/default.png')
    profile_image = CloudinaryField('image', blank=True, null=True, default='profile_images/default.png')
    bio = models.TextField(blank=True)
    # phone_number = models.CharField(blank=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)

    def __str__(self):
        return self.username
 