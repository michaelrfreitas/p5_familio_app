from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from member.models import CustomUser
from django.contrib import messages

# Create your views here.


@login_required(redirect_field_name='account_login')
def plans(request):
    """ A view to return the plans page """
    return render(request, 'subscriber/plans.html')


@login_required(redirect_field_name='account_login')
def subscribed(request, user_id):
    """ Member approves and desapproves to Familio member. """
    subscribe = get_object_or_404(CustomUser, id=user_id)
    subscribe.subscription = not subscribe.subscription
    subscribe.save()
    messages.success(
        request, f'You changed your plan successfully!')  # noqa
    return redirect('plans')
