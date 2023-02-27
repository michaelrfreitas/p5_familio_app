from django.urls import path
from . import views

urlpatterns = [
    path('plans', views.plans, name='plans'),
    path('subscribed/<user_id>', views.subscribed, name='subscribed'),
    path('config/', views.stripe_config),
    path('create-checkout-session/', views.create_checkout_session),
    path('webhook/', views.stripe_webhook),
    path('cancel/', views.stripe_cancel),
]
