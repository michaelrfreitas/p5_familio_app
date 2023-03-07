from django.shortcuts import render, HttpResponse


def home(request):
    """ A view to return the home page """
    return render(request, 'home/home.html')


def contact(request):
    """ A view to return the contact page """
    return render(request, 'home/contact.html')


def sitemap(request):
    f = open('sitemap.xml', 'r')
    file_content = f.read()
    f.close()
    return HttpResponse(file_content, content_type="text/xml")


def robots(request):
    f = open('robots.txt', 'r')
    file_content = f.read()
    f.close()
    return HttpResponse(file_content, content_type="text/plain")
