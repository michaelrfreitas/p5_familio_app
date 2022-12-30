from django.shortcuts import render

# Create your views here.


@login_required(redirect_field_name='account_login')
def plans(request):
    """ A view to return the plans page """
    return render(request, 'subscriber/plans.html')
