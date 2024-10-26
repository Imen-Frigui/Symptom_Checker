from django.shortcuts import render

# Create your views here.

def index(request):
    return render(request, 'front_office/index.html')

def about(request):
    return render(request, 'front_office/about.html')

def contact(request):
    return render(request, 'front_office/contact.html')

def blog(request):
    return render(request, 'front_office/blog.html')

def dashboard(request):
    return render(request, 'back_office/pages/dashboard.html')


  

