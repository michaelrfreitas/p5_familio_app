
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from . import models
from . import forms
from django.contrib import messages
from django.core.mail import EmailMessage


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
    if request.method == 'POST':
        form = forms.MyFamilioForm(request.POST)
        if form.is_valid():
            element = form.save(commit=False)
            element.member = request.user
            element.save()
            # Render the HTML template
            html_content = render(request, 'emails/email_invite.html', {
                'member_name': request.user.first_name,
                'kinship': element.kinship,
                'familio_id': element.id})
            # Create the email message
            subject, from_email, to = 'Familio Invite', 'familio.uk@gmail.com', element.email
            text_content = f'Join your family member { request.user.first_name } that have invited you with a kinship that you are { element.kinship }.'
            msg = EmailMessage(subject, html_content, from_email, [to])
            msg.content_subtype = "html"  # Main content is now text/html
            msg.send()
            messages.success(request, 'The invite was sent successfully!')
            return redirect('menu')
        else:
            messages.warning(request, 'This invite could not be sent.')
    form = forms.MyFamilioForm()
    context = {
        'form': form
    }
    return render(request, 'member/familio.html', context)
