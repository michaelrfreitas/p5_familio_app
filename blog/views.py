from django.shortcuts import render

# Create your views here.


@login_required(redirect_field_name='account_login')
def blog(request):
    """ A view to return the blog page """
    return render(request, 'blog/blog.html')


@login_required(redirect_field_name='account_login')
def pictures(request):
    """ A view to return the pictures page """
    return render(request, 'blog/pictures.html')
