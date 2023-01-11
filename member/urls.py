from django.urls import path
from . import views

urlpatterns = [
    path('delete_member/<user_id>', views.delete_member, name='delete_member'),
    path('menu', views.menu, name='menu'),
    path('familio', views.familio, name='familio'),
    path('tree', views.tree, name='tree'),
    path('group', views.group, name='group'),
    path('approved/<familio_id>', views.approved, name='approved'),
]
