from django.shortcuts import render, get_object_or_404, redirect
from .models import HealthCareInstitution, HealthcareRecommender
from .forms import HealthCareInstitutionForm
from geopy.distance import great_circle
import requests
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import google.generativeai as genai
import json
import os

# Mapping of symptoms to healthcare institution types
SYMPTOM_INSTITUTION_MAP = {
    'headache': ['clinic', 'hospital'],
    'fever': ['clinic', 'hospital'],
    'chest pain': ['hospital'],
    'stomach pain': ['clinic', 'hospital', 'diagnostic_center'],
    'accident': ['emergency room', 'urgent care', 'primary care physician'],
    'cold': ['clinic', 'urgent care'],  # Added cold symptom mapping
    # Add more symptoms and corresponding institution types as needed
}

# Constants
MAX_DISTANCE = 10  # Example maximum distance in kilometers


genai.configure(api_key='AIzaSyCD6sPOCPgRoL7lUr5RsP1taPF85vFWLVM')  # Replace with your actual API key

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

# Front office list of Health Care Institutions
def institution_list_front(request):
    institutions = HealthCareInstitution.objects.all()  # Fetch institutions if necessary
    return render(request, 'front_office/institution.html', {'institutions': institutions})

# View a specific Health Care Institution
def institution_detail(request, pk):
    institution = get_object_or_404(HealthCareInstitution, pk=pk)
    return render(request, 'back_office/pages/institutions/institution_detail.html', {'institution': institution})

# View a specific Health Care Institution in the front office
def institution_detail_front(request, pk):
    institution = get_object_or_404(HealthCareInstitution, pk=pk)
    return render(request, 'front_office/institution-details.html', {'institution': institution})

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
# This is just an example; adjust the functionality as needed
def recommend_institution(request):
    if request.method == 'POST':
        # Implementation here, similar to recommend_institution logic
        return JsonResponse({'reply': 'Your recommendation logic here.'})
    return JsonResponse({'error': 'Invalid request'}, status=400)

# Find nearby institutions
def find_nearby_institutions(request):
    nearest_institutions = None
    if request.method == 'POST':
        latitude = float(request.POST.get('latitude'))
        longitude = float(request.POST.get('longitude'))
        user_location = (latitude, longitude)

        # Fetch all institutions
        institutions = HealthCareInstitution.objects.all()

        # Calculate distances and filter by maximum distance
        institutions_with_distance = []
        for institution in institutions:
            if institution.latitude and institution.longitude:
                institution_location = (institution.latitude, institution.longitude)
                distance = great_circle(user_location, institution_location).kilometers
                if distance <= MAX_DISTANCE:  # Ensure distance is within threshold
                    institutions_with_distance.append({
                        'institution': institution,
                        'distance': distance,
                    })

        # Sort by distance
        institutions_with_distance.sort(key=lambda x: x['distance'])
        nearest_institutions = institutions_with_distance

    return render(request, 'front_office/find_nearby_institutions.html', {
        'nearest_institutions': nearest_institutions,
    })

# A view to render the chatbot interface
def chatbot_view(request):
    return render(request, 'front_office/chatbot-institution.html')  # Template for chatbot


def open_chatbot(request):
    print("hello")  # Ensure correct indentation



@csrf_exempt  # Use cautiously in production
def chatbot_reply(request):
    if request.method == 'POST':
        try:
            user_message = json.loads(request.body).get('message', '')  # Get the user message
            
            # Check for symptoms in user_message
            institutions = []
            for symptom in SYMPTOM_INSTITUTION_MAP.keys():
                if symptom in user_message.lower():
                    institutions.extend(SYMPTOM_INSTITUTION_MAP[symptom])

            if institutions:
                # Generate a response using a predefined message template
                response_message = (
                    f"I'm sorry to hear you're experiencing symptoms related to '{user_message}'. "
                    "Based on your symptoms, I recommend the following healthcare institutions:\n"
                )
                response_message += '\n'.join(f"- {institution.capitalize()}" for institution in set(institutions))

                # You can also call the Gemini API for a more detailed response if needed
                prompt = f"Generate a supportive message about seeking medical help for: {user_message}. Recommendations: {response_message}"
                ai_response = genai.GenerativeModel('gemini-1.5-flash').generate_content(prompt)
                
                reply = ai_response.text  # Use the response from AI
            else:
                reply = "I'm sorry, but I couldn't determine a specific type of institution for your symptoms. Please consult a medical professional."

            return JsonResponse({'reply': reply})  # Return the AI response as JSON

        except Exception as e:
            # Log the error to your console or file with traceback
            import traceback
            print(f"Error processing request: {e}")
            print(traceback.format_exc())  # Print the full traceback
            return JsonResponse({'error': 'An internal error occurred'}, status=500)

    return JsonResponse({'error': 'Invalid request'}, status=400)
