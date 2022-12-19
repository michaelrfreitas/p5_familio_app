from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    phone = models.CharField(max_length=20, blank=True, null=True)
    dob = models.DateField(null=True)
    photo = models.ImageField(
        upload_to='media/', blank=True, null=True, default="")
    subscription = models.BooleanField(default=False)
