from django.shortcuts import render, get_object_or_404, redirect
from .models import HealthCareInstitution
from .forms import HealthCareInstitutionForm

# Create a new Health Care Institution
def create_institution(request):
    if request.method == 'POST':
        form = HealthCareInstitutionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('institution_list')  # Redirect to the list of institutions
    else:
        form = HealthCareInstitutionForm()
    return render(request, 'back_office/pages/institutions/create_institution.html', {'form': form})

# List all Health Care Institutions
def institution_list(request):
    institutions = HealthCareInstitution.objects.all()
    return render(request, 'back_office/pages/institutions/institution_list.html', {'institutions': institutions})

# View a specific Health Care Institution
def institution_detail(request, pk):
    institution = get_object_or_404(HealthCareInstitution, pk=pk)
    return render(request, 'back_office/pages/institutions/institution_detail.html', {'institution': institution})

# Update a specific Health Care Institution
def update_institution(request, pk):
    institution = get_object_or_404(HealthCareInstitution, pk=pk)
    if request.method == 'POST':
        form = HealthCareInstitutionForm(request.POST, instance=institution)
        if form.is_valid():
            form.save()
            return redirect('institution_detail', pk=institution.pk)
    else:
        form = HealthCareInstitutionForm(instance=institution)
    return render(request, 'back_office/pages/institutions/update_institution.html', {'form': form})

# Delete a specific Health Care Institution
def delete_institution(request, pk):
    institution = get_object_or_404(HealthCareInstitution, pk=pk)
    if request.method == 'POST':
        institution.delete()
        return redirect('institution_list')  # Redirect to the list of institutions
    return render(request, 'back_office/pages/institutions/delete_institution.html', {'institution': institution})
