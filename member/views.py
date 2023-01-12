
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from . import models
from . import forms
from django.contrib import messages
from django.core.mail import send_mail


@login_required(redirect_field_name='account_login')
def delete_member(request, user_id):
    member = get_object_or_404(models.CustomUser, id=user_id)
    member.delete()
    return redirect('account_login')


@login_required(redirect_field_name='account_login')
def tree(request):
    """ A view to return the tree page """
    return render(request, 'member/tree.html')


@login_required(redirect_field_name='account_login')
def group(request):
    """ A view to return the menu page """
    return render(request, 'member/group.html')


@login_required(redirect_field_name='account_login')
def menu(request):
    """ A view to return the menu page """
    return render(request, 'member/menu.html')


@login_required(redirect_field_name='account_login')
def familio(request):
    """ 
    Member send a invite to a probably family member, 
    that didn't be part of their family yet. 
    """
    if request.method == 'POST':
        form = forms.MyFamilioForm(request.POST)
        if form.is_valid():
            element = form.save(commit=False)
            element.member = request.user
            element.save()
            # Create the email message
            subject, from_email, to = '[Familio] Invite', 'familio.uk@gmail.com', element.email
            text_content = (
                f"Hello, We are Familio and we have a invite to you.\n\n"
                f"Join your family member { request.user.first_name } { request.user.last_name } "
                f"that has invited you as a family to be part of Familio.\n\n"
                f"This tool will help you to be close to your family.\n\n"
                f"Do you want to accept Michael Freitas's invitation?\n\n"
                f"Click or copy the link in the browser.\n\n"
                f"{ request.activate_url}/members/approved/{ element.id }\n\n"
                f"Many thanks!\nRegards!"
            )
            send_mail(
                subject,
                text_content,
                from_email,
                [to],
                fail_silently=False,
            )
            messages.success(request, 'The invite was sent successfully!')
            return redirect('familio')
        else:
            messages.warning(request, 'This invite could not be sent.')
    form = forms.MyFamilioForm()
    familios = models.Familio.objects.filter(member=request.user)
    receives = models.Familio.objects.filter(email=request.user.email)
    context = {
        'form': form,
        'familios': familios,
        'receives': receives
    }
    return render(request, 'member/familio.html', context)


@login_required(redirect_field_name='account_login')
def approved(request, familio_id):
    """ Member approves to Familio member. """
    approve = get_object_or_404(models.Familio, id=familio_id)
    approve.approved = not approve.approved
    approve.save()
    messages.success(request, 'The invite was been approved!')
    return redirect('familio')
