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
    ('Son', 'Son'),
    ('Daughter', 'Daughter'),
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
    stripeCustomerId = models.CharField(max_length=255, default="")
    stripeSubscriptionId = models.CharField(max_length=255, default="")

    def __str__(self):
        return f'{self.first_name} {self.last_name}'


class Familio(models.Model):
    level = models.CharField(max_length=20, choices=LEVEL)
    member = models.ForeignKey(User, on_delete=models.CASCADE)
    kinship = models.CharField(max_length=20, choices=KINSHIP)
    email = models.EmailField(default="", blank=True, null=True)
    approved = models.BooleanField(default=False)
    created_on = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=50, default='')

    class Meta:
        ordering = ['name']

    def __str__(self):
        return f'{self.name} - {self.kinship}'


class Group(models.Model):
    familio = models.ManyToManyField(Familio)
    grp_name = models.CharField(max_length=50, null=False)
    created_on = models.DateTimeField(auto_now_add=True)
    member = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        ordering = ['created_on']

    def get_familios(self):
        names = [f.name for f in self.familio.all()]
        return ', '.join(names)

    def __str__(self):
        return self.grp_name
