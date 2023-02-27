from django.urls import path
from . import views

urlpatterns = [
    path('delete_member/<user_id>', views.delete_member, name='delete_member'),
    path('menu', views.menu, name='menu'),
    path('familio', views.familio, name='familio'),
    path('tree', views.tree, name='tree'),
    path('group', views.group, name='group'),
    path('approved/<familio_id>', views.approved, name='approved'),
    path('edit_invite/<familio_id>', views.edit_invite, name='edit_invite'),
    path('delete_invite/<familio_id>', views.delete_invite, name='delete_invite'),
    path('my_profile', views.my_profile, name='my_profile'),
]
