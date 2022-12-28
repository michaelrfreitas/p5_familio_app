from django.contrib import admin
from . import models


@admin.register(models.CustomUser)
class UserAdmin (admin.ModelAdmin):
    list_display = ('username', 'first_name', 'last_name',
                    'email', 'dob', 'subscription')
    list_filter = ('subscription', 'dob')
    search_fields = ('first_name', 'last_name', 'username',
                     'email', 'dob')


@admin.register(models.Familio)
class FamilioAdmin (admin.ModelAdmin):
    list_display = ('email', 'kinship', 'level',
                    'member', 'approved', 'created_on')
    list_filter = ('kinship', 'level', 'approved', 'created_on')
    search_fields = ('email', 'member', 'kinship')


@admin.register(models.Group)
class GroupAdmin (admin.ModelAdmin):
    list_display = ('grp_name', 'created_on')
    list_filter = ('familio', 'created_on')
    search_fields = ('grp_name',)
