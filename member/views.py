
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import CustomUser


@login_required(redirect_field_name='account_login')
def delete_member(request, user_id):
    member = get_object_or_404(CustomUser, id=user_id)
    member.delete()
    return redirect('account_login')
