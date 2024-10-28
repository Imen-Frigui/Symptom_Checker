from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from users.decorators import role_required
from Institution.models import HealthCareInstitution  # Import your model

# Create your views here.


# def index(request):
#     institutions = HealthCareInstitution.objects.all()  
#     return redirect('diagnose', {'institutions': institutions})
def index(request):
    institutions = HealthCareInstitution.objects.all()  
    return render(request, 'front_office/index.html', {'institutions': institutions})


@login_required
@role_required('simple')
def about(request):
    return render(request, 'front_office/about.html')

def contact(request):
    return render(request, 'front_office/contact.html')

def blog(request):
    return render(request, 'front_office/blog.html')

# Admin-only view
# @login_required
# def dashboard(request):
#     return render(request, 'back_office/pages/dashboard.html')


# Main index page
# def index(request):
#     institutions = HealthCareInstitution.objects.all()  # Fetch all institutions
#     return render(request, 'front_office/index.html', {'institutions': institutions})  # Pass institutions to the template
  


# Main index page
# def index(request):
#     institutions = HealthCareInstitution.objects.all()  # Fetch all institutions
#     return render(request, 'front_office/index.html', {'institutions': institutions})  # Pass institutions to the template
  

# Admin-only view
@login_required
def dashboard(request):
    return render(request, 'back_office/pages/dashboard.html')