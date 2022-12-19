from django.contrib import admin

from .models import CustomUser


@admin.register(CustomUser)
class UserAdmin (admin.ModelAdmin):
    list_display = ('username', 'first_name', 'last_name',
                    'email', 'dob', 'subscription')
    list_filter = ('subscription', 'dob')
    search_fields = ('first_name', 'last_name', 'username',
                     'email', 'dob')
