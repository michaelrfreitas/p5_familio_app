from django.urls import path
from . import views

urlpatterns = [
    path('plans', views.plans, name='plans'),
    path('subscribed/<user_id>', views.subscribed, name='subscribed'),
]
