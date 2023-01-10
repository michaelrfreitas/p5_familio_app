from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings

User = settings.AUTH_USER_MODEL

LEVEL = (
    ('Close Family', 'Close Family'),
    ('Family Around', 'Family Around'),
    ('Away Family', 'Away Family'),
)

KINSHIP = (
    ('Mother', 'Mother'),
    ('Father', 'Father'),
    ('Brother', 'Brother'),
    ('Sister', 'Sister'),
    ('Wife', 'Wife'),
    ('Husband', 'Husband'),
    ('Cousin', 'Cousin'),
    ('Aunt', 'Aunt'),
    ('Uncle', 'Uncle'),
    ('Nephew', 'Nephew'),
    ('Niece', 'Niece'),
    ('Grandmother', 'Grandmother'),
    ('Grandfather', 'Grandfather'),
    ('Great-grandmother', 'Great-grandmother'),
    ('Great-grandfather', 'Great-grandfather'),
    ('Brother-in-law', 'Brother-in-law'),
    ('Sister-in-law', 'Sister-in-law'),
    ('Mother-in-law', 'Mother-in-law'),
    ('Father-in-law', 'Father-in-law'),
)


class CustomUser(AbstractUser):
    phone = models.CharField(max_length=20, blank=True, null=True)
    dob = models.DateField(null=True)
    photo = models.ImageField(
        upload_to='static/media/', blank=True, null=True, default="")
    subscription = models.BooleanField(default=False)


class Familio(models.Model):
    level = models.CharField(max_length=20, choices=LEVEL)
    member = models.ForeignKey(User, on_delete=models.CASCADE)
    kinship = models.CharField(max_length=20, choices=KINSHIP)
    email = models.EmailField(null=False)
    approved = models.BooleanField(default=False)
    created_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_on']


class Group(models.Model):
    familio = models.ForeignKey(Familio, on_delete=models.CASCADE)
    grp_name = models.CharField(max_length=50, null=False)
    created_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_on']
