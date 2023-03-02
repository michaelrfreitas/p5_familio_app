from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib import messages

# Create your views here.


@login_required(redirect_field_name='account_login')
def blog(request):
    """ A view to return the blog page """
    return render(request, 'blog/blog.html')


@login_required(redirect_field_name='account_login')
def pictures(request):
    if request.user.subscription:
        """ A view to return the pictures page """
        return render(request, 'blog/pictures.html')
    else:
        messages.info(request, 'You are using a free plan and can not access this')
        return render(request, 'member/menu.html')
