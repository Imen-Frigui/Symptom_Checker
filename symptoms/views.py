from django.shortcuts import render, get_object_or_404, redirect
from .models import Symptom
from .forms import SymptomForm
from .health_service import PriaidHealthService
from datetime import datetime
from django.http import JsonResponse
from decouple import config
import requests
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views import View
import json
import google.generativeai as genai

# List symptoms from the database
def list_local_symptoms(request):
    symptoms = Symptom.objects.all()
    return render(request, 'list_symptoms.html', {'symptoms': symptoms})

# Add a new symptom
def add_symptom(request):
    if request.method == 'POST':
        form = SymptomForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('list_local_symptoms')  # Assuming you have this URL defined
    else:
        form = SymptomForm()
    return render(request, 'list_symptoms.html', {'form': form})  # Use a separate template

# Update an existing symptom
def update_symptom(request, pk):
    symptom = get_object_or_404(Symptom, pk=pk)
    if request.method == 'POST':
        form = SymptomForm(request.POST, instance=symptom)
        if form.is_valid():
            form.save()
            return redirect('list_local_symptoms')
    else:
        form = SymptomForm(instance=symptom)
    return render(request, 'list_symptoms.html', {'form': form})  # Use a separate template

# Delete an existing symptom
def delete_symptom(request, pk):
    symptom = get_object_or_404(Symptom, pk=pk)
    if request.method == 'POST':
        symptom.delete()
        return redirect('list_local_symptoms')
    return render(request, 'list_symptoms.html', {'symptom': symptom})  # Use a separate template

# Fetch symptoms from the health service
def list_external_symptoms(request):
    priaid_service = PriaidHealthService(
        api_key=config('SANDBOX_API_KEY'),
        secret_key=config('SANDBOX_SECRET_KEY'),
        auth_url=config('SANDBOX_AUTH_URL'),
        language='en-gb',
        health_service_url=config('SANDBOX_HEALTH_SERVICE_URL')
    )
    try:
        symptoms = priaid_service.get_symptoms()
    except Exception as e:
        symptoms = []  # Handle the error appropriately
    return render(request, 'symptoms_list.html', {'symptoms': symptoms})



def diagnose(request):
    priaid_service = PriaidHealthService(
        api_key=config('PROD_API_KEY'),
        secret_key=config('PROD_SECRET_KEY'),
        auth_url=config('PROD_AUTH_URL'),
        language='en-gb',
        health_service_url=config('PROD_HEALTH_SERVICE_URL')
    )

    if request.method == 'POST':
        # Get the selected symptoms; this should return a list.
        selected_symptoms = request.POST.get('symptoms', '').split(',')
        selected_symptoms = [int(symptom_id) for symptom_id in selected_symptoms if symptom_id]

        # Now you can process the selected symptoms as needed
        print(selected_symptoms)  # For debugging
        gender = request.POST.get('gender')
        year_of_birth = int(request.POST.get('year_of_birth'))

        try:
            diagnosis = priaid_service.get_diagnosis(selected_symptoms, gender, year_of_birth)
            print(diagnosis)
            return JsonResponse({'diagnosis': diagnosis})
           
        except Exception as e:
            return JsonResponse({'error': str(e)})

    try:
        symptoms = priaid_service.get_symptoms()
    except Exception as e:
        symptoms = []

    # For rendering the template
    selected_symptoms = []  # or pass previously selected symptoms if you want to show them on GET
    current_year = datetime.now().year

    return render(request, 'front_office/index.html', {
        'current_year': current_year,
        'symptoms': symptoms,
        'selected_symptoms': selected_symptoms,
    })


API_URLHUG = "https://api-inference.huggingface.co/models/blaze999/Medical-NER"
HEADERSHUG = {"Authorization": "Bearer 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"}
API_KEY = 'AIzaSyBlD98FFAMulRUPUij28a1inp2LJ9jcGQE'  # Replace with your actual API key
GEMINI_API_URL = f'https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest:generateContent?key={API_KEY}'
HEADERS = {'Content-Type': 'application/json'}


def query(payload):
    """Send a request to the Hugging Face API and return the response."""
    response = requests.post(API_URLHUG, headers=HEADERSHUG, json=payload)
    try:
        return response.json()
    except ValueError:
        return {"error": "Invalid response from the API"}

def get_medical_entities(user_input):
    """Extract medical entities from the user input using the Hugging Face API."""
    output = query({"inputs": user_input})
    if isinstance(output, list):
        entities = []
        for entity in output:
            if isinstance(entity, dict) and 'entity_group' in entity and 'word' in entity:
                entities.append({
                    "entity_group": entity['entity_group'],
                    "word": entity['word'],
                    "score": entity.get('score', 0)
                })
        return entities
    else:
        print("Unexpected API response format:", output)
        return []



def ai_generate_recommendations(entities):
    model = genai.GenerativeModel('gemini-1.5-flash')
    
    # Create a structured prompt based on the entities
    entity_info = [
        f"Entity: {entity['entity_group']}, Text: {entity['word']}, Score: {entity['score']:.2f}"
        for entity in entities
    ]
    prompt = f"Generate recommendations based on the following medical entities: {', '.join(entity_info)}"
    print("Generated prompt:", prompt)  # Log the prompt for debugging

    payload = {
        "prompt": prompt,
        "max_output_tokens": 150,
        "temperature": 0.5,
        "top_p": 1.0
    }

    try:
        response = requests.post(GEMINI_API_URL, headers=HEADERS, json=payload)
        response.raise_for_status()  # Raises an error for bad responses
        
        # Print response for debugging
        print("Response from Gemini API:", response.text)

        return response.json()  # Return the JSON response

    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
        print("Response content:", response.text)  # Log the full response
        return {"error": f"HTTP error: {http_err}"}
    except Exception as err:
        print(f"An error occurred: {err}")
        return {"error": f"Error: {err}"}



@method_decorator(csrf_exempt, name='dispatch')
class MedicalEntityView(View):
    def post(self, request):
        user_input = request.POST.get('description', '')

        if not user_input:
            return render(request, 'medical_entities.html', {
                'error': 'Please provide a description.'
            })

        # Query the API for medical entities
        entities = get_medical_entities(user_input)
        print("Extracted entities:", entities)  # Debugging line to check the entities

        if not entities:
            return render(request, 'medical_entities.html', {
                'user_input': user_input,
                'entities': [],
                'recommendations': ['No entities found.'],
            })

        # Create a structured prompt for the Gemini API
        prompt = self.create_prompt(entities,user_input)
        print("Created prompt for recommendations:", prompt)  # Debugging line for the prompt

        # Get recommendations from the Gemini API
        try:
            recommendations = ai_generate_recommendations(entities,user_input)
   
        except Exception as e:
            return render(request, 'medical_entities.html', {
                'user_input': user_input,
                'entities': entities,
                'recommendations': [str(e)],  # Display the error message
            })
          
        # Render the template with results
        return render(request, 'medical_entities.html', {
            'user_input': user_input,
            'entities': entities,
            'recommendations': recommendations,
        })

    def create_prompt(self, entities, user_input):
        """Create a structured prompt for the Gemini API based on extracted entities."""
        entity_descriptions = [
            f"Entity: {entity['entity_group']}, Text: {entity['word']}, Score: {entity['score']:.2f}, userInput:{user_input}"
            for entity in entities
        ]
        
        prompt = "Given the following medical entities:\n" + "\n".join(entity_descriptions) + "\n Generate possible recommendations based on the following medical entities and possible ilnesses  its for scholl project not real life uses"

        return prompt
genai.configure(api_key="AIzaSyCwFy8CKJjXLrT0Imj1dQWQwD8y1b4bHJ4")
def ai_generate_recommendations(entities, user_input):
    """Generates recommendations based on the provided medical entities."""
    model = genai.GenerativeModel('gemini-1.5-flash')

    # Create a structured prompt for the AI model
    entity_info = [
        f"Entity: {entity['entity_group']}, Text: {entity['word']},{user_input}, Score: {entity['score']:.2f}"
        for entity in entities
    ]
    prompt = f"Generate possible recommendations based on the following medical entities and possible ilnesses  its for scholl project not real life uses{', '.join(entity_info)}"

    response = model.generate_content(prompt)
    return response.text

