from django.urls import path
from . import views

urlpatterns = [
    path('delete_member/<user_id>', views.delete_member, name='delete_member'),
]
