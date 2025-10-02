from django.db import models
# from django.contrib.auth.models import User
from django.conf import settings

class Event(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    date = models.DateField()
    time = models.TimeField()
    location = models.CharField(max_length=255)
    category = models.ForeignKey(
        "Category",
        on_delete=models.CASCADE,
        default=1
    )
    asset = models.ImageField(upload_to='events_asset', blank=True, null=True, default="events_asset/default-image.jpg")
    assign_to = models.ManyToManyField(
        # User,
        settings.AUTH_USER_MODEL,
        related_name="events",
        blank=True,
        # null=True
    )
    rsvp = models.ManyToManyField(
        # User, 
        settings.AUTH_USER_MODEL,
        related_name="rsvp_events", 
        blank=True 
    )

class Category(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name
