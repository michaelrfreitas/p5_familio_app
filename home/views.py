from django.shortcuts import render


def home(request):
    """ A view to return the home page """
    return render(request, 'home/home.html')


def contact(request):
    """ A view to return the contact page """
    return render(request, 'home/contact.html')
