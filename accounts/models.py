from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    address = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=20)
    profile_picture = models.ImageField(
        upload_to="profile_pics/", blank=True, null=True
    )
    order_count = models.IntegerField(default=0)
