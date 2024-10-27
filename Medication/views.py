import os
import io
import requests
import json
import google.generativeai as genai
from django.http import HttpResponse, JsonResponse, HttpResponseBadRequest
from django.shortcuts import render, redirect, get_object_or_404
from .models import Medication, SideEffect, Treatment , Feedback
from .forms import MedicationForm, SideEffectForm, TreatmentForm , FeedbackForm
from django.core.paginator import Paginator 
from django.db.models import Q 
from django.views.decorators.csrf import csrf_exempt
from django.db import models
from textblob import TextBlob  
from django.views.decorators.http import require_POST



GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')
genai.configure(api_key=GOOGLE_API_KEY)

# generate description using Google Gemini API
def generate_medication_description(name):
    model = genai.GenerativeModel('gemini-1.5-flash')
    prompt = f"Generate a detailed description for a medication called {name} in 3-4 lines."
    
    response = model.generate_content(prompt)
    if response and hasattr(response, 'text'):
        return response.text
    return "Description not available."

@csrf_exempt
def generate_description_api(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            print("Received data:", data)  
            medication_name = data.get("medication_name", "")

            if not medication_name:
                return HttpResponseBadRequest("Medication name is required.")

            description = generate_medication_description(medication_name)
            return JsonResponse({"description": description})

        except json.JSONDecodeError as e:
            print("JSON decode error:", e)
            return HttpResponseBadRequest("Invalid JSON format.")
    return HttpResponseBadRequest("Invalid request method")

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
    search_query = request.GET.get('search', '')

    treatments_list = Treatment.objects.filter(
        Q(name__icontains=search_query) |
        Q(description__icontains=search_query)
    ).distinct()

    paginator = Paginator(treatments_list, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

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
    


def side_effect_severity_chart(request):
    # Fetch all side effects with their descriptions and severity scores
    side_effects = list(SideEffect.objects.values('description', 'severity_score', 'severity_label'))
    return render(request, 'medication/side_effect_severity_chart.html', {'side_effects': json.dumps(side_effects)})


def run_analysis(request):
    # Run the severity analysis for all side effects in the database
    side_effects = SideEffect.objects.all()
    for side_effect in side_effects:
        analysis_result = analyze_side_effect_severity(side_effect.description)
        side_effect.severity_label = analysis_result['label']
        side_effect.severity_score = analysis_result['score']
        side_effect.save()
    
    return redirect('side_effect_severity_chart') 


def treatment_and_medication_list(request):
    # Get the search query from the GET parameters
    query = request.GET.get('q', '')

    # Fetch all treatments and apply search filter
    treatments = Treatment.objects.prefetch_related('medications__side_effects').all()
    if query:
        treatments = treatments.filter(
            models.Q(name__icontains=query) |
            models.Q(description__icontains=query) |
            models.Q(medications__name__icontains=query) |
            models.Q(medications__description__icontains=query) |
            models.Q(medications__side_effects__description__icontains=query)
        ).distinct()

    # Paginate the treatments
    paginator = Paginator(treatments, 3)  
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)


  # Instantiate the Feedback form
    feedback_form = FeedbackForm()

    return render(request, 'medication/treatment_and_medication_list.html', {
        'page_obj': page_obj,
        'query': query,
        'feedback_form': feedback_form,
    })

    
def submit_feedback(request, pk):
    treatment = get_object_or_404(Treatment, pk=pk)
    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            feedback = form.save(commit=False)
            feedback.treatment = treatment

            # Calculate sentiment score using TextBlob
            analysis = TextBlob(feedback.feedback_text)
            feedback.sentiment_score = analysis.sentiment.polarity  # Range: -1 (negative) to 1 (positive)
            
            feedback.save()
            
            # Return the feedback text and sentiment score as JSON
            return JsonResponse({
                'feedback_text': feedback.feedback_text,
                'sentiment_score': feedback.sentiment_score
            })

    # If the form is invalid, return an error response
    return JsonResponse({'error': 'Invalid feedback'}, status=400)