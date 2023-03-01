import json
import os
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from . import models
from . import forms
from subscriber.views import stripe_cancel
from django.contrib import messages
from django.core.mail import send_mail
from django.conf.urls.static import static


@login_required(redirect_field_name='account_login')
def delete_member(request, user_id):
    if request.method == 'POST':
        member = get_object_or_404(models.CustomUser, id=user_id)
        models.Familio.objects.filter(email=member.email).delete()
        if member.subscription:
            stripe_cancel(request)
        member.delete()
        return redirect('account_login')
    return render(request, 'member/delete.html')


@login_required(redirect_field_name='account_login')
def my_profile(request):
    """ Member edit their profiles """
    member = get_object_or_404(models.CustomUser, id=request.user.id)
    if request.method == 'POST':
        form = forms.MyCustomUserForm(
            request.POST, request.FILES, instance=member)
        if form.is_valid():
            form.save()
            return redirect('my_profile')
        else:
            messages.warning(request, 'This profile could not be updated.')
    form = forms.MyCustomUserForm(instance=member)
    context = {
        'form': form,
    }
    return render(request, 'member/my_profile.html', context)


@login_required(redirect_field_name='account_login')
def tree(request):
    """ Creating a Family Tree """
    # Array with all invites sent to members
    familios = models.Familio.objects.filter(member=request.user)
    # Array with all invites received from members
    receives = models.Familio.objects.filter(email=request.user.email)
    # Data Array to create a JSON file with details
    data = []
    # Variables
    pid = ''
    ppid = ''
    tag = ''
    pid_main = ''
    ppid_main = ''
    tag_main = ''
    # Check if there is image in the main profile
    if request.user.photo == '':
        my_img = ''
    else:
        my_img = request.user.photo.url
    # Loop to collect all data in familio relationship
    for familio in familios:
        # Check if the familio relationship is approved
        if familio.approved:
            # Collect specific members details from each familio member
            member = get_object_or_404(models.CustomUser, email=familio.email)
            # If have a Father kinship
            if familio.kinship == 'Father':
                ppid_main = member.id
            # If have a Mother kinship
            elif familio.kinship == 'Mother':
                pid_main = member.id
                tag_main = 'childrenTemplate'
    # Add data regarding main profile to Data Array
    data.append({
                'id': request.user.id,
                'pid': pid_main,
                'ppid': ppid_main,
                'name': request.user.first_name + ' ' + request.user.last_name,
                'parent': 'Myself',
                'img': my_img,
                'tags': [tag_main],
                })
    # Loop to collect all data in familio relationship
    for familio in familios:
        # Check if the familio relationship is approved
        if familio.approved:
            # Collect specific members details from each familio member
            member = get_object_or_404(models.CustomUser, email=familio.email)
            # Check if there is image in the profiles
            if member.photo == '':
                img = ''
            else:
                img = member.photo.url
            # If have a Father kinship
            if familio.kinship == 'Father':
                pid = pid_main
                ppid = ''
                tag = 'partner'
            elif familio.kinship == 'Mother':
                pid = ''
                ppid = ''
                tag = ''
            elif familio.kinship == 'Brother' or familio.kinship == 'Sister':
                pid = pid_main
                ppid = ppid_main
                tag = tag_main
            elif familio.kinship == 'Wife' or familio.kinship == 'Husband':
                pid = request.user.id
                tag = 'partner'
                ppid = ''
                ppid_p = member.id
            elif familio.kinship == 'Son' or familio.kinship == 'Daughter':
                pid = request.user.id
                tag = 'childrenTemplate'
                ppid = ppid_p
            else:
                tag = ''
                pid = ''
                ppid = ''
            # Add the data compiled to the Data Array for JSON file
            data.append({
                'id': member.id,
                'pid': pid,
                'ppid': ppid,
                'name': member.first_name + ' ' + member.last_name,
                'parent': familio.kinship,
                'img': img,
                'tags': [tag],
            })
    path = 'static/json'
    file = f'{request.user.email}.json'
    out_file = open(os.path.join(path, file), "w")
    out_file.write('')
    json.dump(data, out_file)
    out_file.close()
    return render(request, 'member/tree.html')


@login_required(redirect_field_name='account_login')
def group(request):
    if request.user.subscription:
        """ A view to return the group page """
        member = get_object_or_404(models.CustomUser, id=request.user.id)
        if request.method == 'POST':
            form = forms.MyGroupForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect('group')
            else:
                messages.warning(request, 'This group can not be created.')
        form = forms.MyGroupForm(my_familio=member)
        context = {
            'form': form,
        }
        return render(request, 'member/group.html', context)
    else:
        messages.info(
            request, 'You are using a free plan and can not access this')
        return render(request, 'member/menu.html')


@login_required(redirect_field_name='account_login')
def menu(request):
    """ A view to return the menu page """
    return render(request, 'member/menu.html')


@login_required(redirect_field_name='account_login')
def familio(request):
    """ Member send a invite to a probably family member
    that didn't be part of their family yet. """
    if request.method == 'POST':
        form = forms.MyFamilioForm(request.POST)
        if form.is_valid():
            element = form.save(commit=False)
            if models.Familio.objects.filter(email=element.email, member=request.user):  # noqa
                messages.warning(
                    request, 'You have already invited this email address. See in list Familio Sent.')  # noqa
                return redirect('familio')
            else:
                if request.user.subscription or models.Familio.objects.filter(member=request.user).count() < 10:
                    element.member = request.user
                    element.save()
                    # Create the email message
                    subject, from_email, to = '[Familio] Invite', 'familio.uk@gmail.com', element.email  # noqa
                    text_content = (
                        f"Hello, We are Familio and we have a invite to you.\n\n"
                        f"Join your family member { request.user.first_name } { request.user.last_name } "  # noqa
                        f"that has invited you as a family to be part of Familio.\n\n"  # noqa
                        f"This tool will help you to be close to your family.\n\n"
                        f"Do you want to accept { request.user.first_name } { request.user.last_name }'s invitation?\n\n"
                        f"Click or copy the link in the browser.\n\n"
                        f"{ request.scheme }://{request.META['HTTP_HOST'] }/members/approved/{ element.id }\n\n"  # noqa
                        f"Many thanks!\nRegards!"
                    )
                    send_mail(
                        subject,
                        text_content,
                        from_email,
                        [to],
                        fail_silently=False,
                    )
                    messages.success(
                        request, 'The invite was sent successfully!')
                    return redirect('familio')
                else:
                    messages.warning(
                        request, 'Unfortunately, We can see that you are in a free plan and have exceeded the limit of 10 members, so we are sending your invite without adding this member to your family.')
                    # Create the email message
                    subject, from_email, to = '[Familio] Invite', 'familio.uk@gmail.com', element.email  # noqa
                    text_content = (
                        f"Hello, We are Familio and we have a invite to you.\n\n"
                        f"Join your family member { request.user.first_name } { request.user.last_name } "  # noqa
                        f"that has invited you as a family to be part of Familio.\n\n"  # noqa
                        f"This tool will help you to be close to your family.\n\n"
                        f"Do you want to accept { request.user.first_name } { request.user.last_name }'s invitation?\n\n"
                        f"Click or copy the link in the browser.\n\n"
                        f"{ request.scheme }://{request.META['HTTP_HOST'] }\n\n"  # noqa
                        f"Many thanks!\nRegards!"
                    )
                    send_mail(
                        subject,
                        text_content,
                        from_email,
                        [to],
                        fail_silently=False,
                    )
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
    """ Member approves and desapproves to Familio member. """
    approve = get_object_or_404(models.Familio, id=familio_id)
    approve.approved = not approve.approved
    approve.save()
    messages.info(
        request, f'The status has changed to Invite member: { approve.member.first_name } { approve.member.last_name } your Kinship: { approve.kinship}!')  # noqa
    return redirect('familio')


@login_required(redirect_field_name='account_login')
def edit_invite(request, familio_id):
    """ Member edit the Familio member invites """
    invite = get_object_or_404(models.Familio, id=familio_id)
    if request.method == 'POST':
        form = forms.MyFamilioForm(request.POST, instance=invite)
        if form.is_valid():
            form.save()
            return redirect('familio')
        else:
            messages.warning(request, 'This invite could not be updated.')
    form = forms.MyFamilioForm(instance=invite)
    familios = models.Familio.objects.filter(member=request.user)
    receives = models.Familio.objects.filter(email=request.user.email)
    context = {
        'form': form,
        'familios': familios,
        'receives': receives
    }
    return render(request, 'member/familio.html', context)


@login_required(redirect_field_name='account_login')
def delete_invite(request, familio_id):
    """  Member delete the Familio member invites """
    invite = get_object_or_404(models.Familio, id=familio_id)
    invite.delete()
    return redirect('familio')
