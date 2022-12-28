
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from . import models
from . import forms
from django.contrib import messages


@login_required(redirect_field_name='account_login')
def delete_member(request, user_id):
    member = get_object_or_404(models.CustomUser, id=user_id)
    member.delete()
    return redirect('account_login')


@login_required(redirect_field_name='account_login')
def menu(request):
    """ A view to return the menu page """
    return render(request, 'member/menu.html')


@login_required(redirect_field_name='account_login')
def familio(request):
    if request.method == 'POST':
        form = forms.MyFamilioForm(request.POST)
        if form.is_valid():
            element = form.save(commit=False)
            element.member = request.user
            element.save()
            return redirect('menu')
        else:
            messages.warning(request, 'This invite is already sent.')
    form = forms.MyFamilioForm()
    context = {
        'form': form
    }
    return render(request, 'member/familio.html', context)
