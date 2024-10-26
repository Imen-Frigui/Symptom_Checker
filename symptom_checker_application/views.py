from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from users.decorators import role_required

# Create your views here.

def index(request):
    return render(request, 'front_office/index.html')

@login_required
@role_required('simple')
def about(request):
    return render(request, 'front_office/about.html')

def contact(request):
    return render(request, 'front_office/contact.html')

def blog(request):
    return render(request, 'front_office/blog.html')

# Admin-only view
@login_required
def dashboard(request):
    return render(request, 'back_office/pages/dashboard.html')

