from django.shortcuts import render, redirect, get_object_or_404
from .models import Medication, SideEffect, Treatment
from .forms import MedicationForm, SideEffectForm, TreatmentForm
from django.core.paginator import Paginator 
from django.db.models import Q 

# Medication Views
def medication_list(request):
    search_query = request.GET.get('search', '')
    medications = Medication.objects.filter(
        Q(name__icontains=search_query) |
        Q(description__icontains=search_query) |
        Q(side_effects__description__icontains=search_query)
    ).distinct()
    paginator = Paginator(medications, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'medication/medication_list.html', {'page_obj': page_obj, 'search_query': search_query})

def medication_detail(request, pk):
    medication = get_object_or_404(Medication, pk=pk)
    return render(request, 'medication/medication_detail.html', {'medication': medication})

def medication_create(request):
    if request.method == 'POST':
        form = MedicationForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('medication_list')
    else:
        form = MedicationForm()
    return render(request, 'medication/medication_form.html', {'form': form})

def medication_update(request, pk):
    medication = get_object_or_404(Medication, pk=pk)
    if request.method == 'POST':
        form = MedicationForm(request.POST, request.FILES, instance=medication)
        if form.is_valid():
            form.save()
            return redirect('medication_list')
    else:
        form = MedicationForm(instance=medication)
    return render(request, 'medication/medication_form.html', {'form': form})

def medication_delete(request, pk):
    medication = get_object_or_404(Medication, pk=pk)
    if request.method == 'POST':
        medication.delete()
        return redirect('medication_list')
    return render(request, 'medication/medication_confirm_delete.html', {'medication': medication})


# SideEffect Views
def sideeffect_list(request):
    sideeffects_list = SideEffect.objects.all()
    paginator = Paginator(sideeffects_list, 5)  
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'medication/sideeffect_list.html', {'page_obj': page_obj})

def sideeffect_create(request):
    if request.method == 'POST':
        form = SideEffectForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('sideeffect_list')
    else:
        form = SideEffectForm()
    return render(request, 'medication/sideeffect_form.html', {'form': form})

def sideeffect_update(request, pk):
    sideeffect = get_object_or_404(SideEffect, pk=pk)
    if request.method == 'POST':
        form = SideEffectForm(request.POST, instance=sideeffect)
        if form.is_valid():
            form.save()
            return redirect('sideeffect_list')
    else:
        form = SideEffectForm(instance=sideeffect)
    return render(request, 'medication/sideeffect_form.html', {'form': form})

def sideeffect_delete(request, pk):
    sideeffect = get_object_or_404(SideEffect, pk=pk)
    if request.method == 'POST':
        sideeffect.delete()
        return redirect('sideeffect_list')
    return render(request, 'medication/sideeffect_confirm_delete.html', {'sideeffect': sideeffect})


# Treatment Views
def treatment_list(request):
    # Get search query from request
    search_query = request.GET.get('search', '')

    # Filter treatments based on search query for name and description
    treatments_list = Treatment.objects.filter(
        Q(name__icontains=search_query) |
        Q(description__icontains=search_query)
    ).distinct()

    # Paginate the treatments list (5 items per page)
    paginator = Paginator(treatments_list, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Pass page_obj and search_query to the template
    return render(request, 'medication/treatment_list.html', {
        'page_obj': page_obj,
        'search_query': search_query
    })

def treatment_create(request):
    if request.method == 'POST':
        form = TreatmentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('treatment_list')
    else:
        form = TreatmentForm()
    return render(request, 'medication/treatment_form.html', {'form': form})

def treatment_update(request, pk):
    treatment = get_object_or_404(Treatment, pk=pk)
    if request.method == 'POST':
        form = TreatmentForm(request.POST, instance=treatment)
        if form.is_valid():
            form.save()
            return redirect('treatment_list')
    else:
        form = TreatmentForm(instance=treatment)
    return render(request, 'medication/treatment_form.html', {'form': form})

def treatment_delete(request, pk):
    treatment = get_object_or_404(Treatment, pk=pk)
    if request.method == 'POST':
        treatment.delete()
        return redirect('treatment_list')
    return render(request, 'medication/treatment_confirm_delete.html', {'treatment': treatment})

def treatment_detail(request, pk):
    treatment = get_object_or_404(Treatment, pk=pk)
    return render(request, 'medication/treatment_detail.html', {'treatment': treatment})