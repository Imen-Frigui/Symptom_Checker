from django.shortcuts import render
from Institution.models import HealthCareInstitution  # Import your model

# Create your views here.

def index(request):
    institutions = HealthCareInstitution.objects.all()  
    return render(request, 'front_office/index.html', {'institutions': institutions})

def about(request):
    return render(request, 'front_office/about.html')

def contact(request):
    return render(request, 'front_office/contact.html')

def blog(request):
    return render(request, 'front_office/blog.html')

def dashboard(request):
    return render(request, 'back_office/pages/dashboard.html')

# Main index page
# def index(request):
#     institutions = HealthCareInstitution.objects.all()  # Fetch all institutions
#     return render(request, 'front_office/index.html', {'institutions': institutions})  # Pass institutions to the template
  

