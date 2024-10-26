import os
import requests
from dotenv import load_dotenv

# Load API Key from environment variables
load_dotenv()
HUGGINGFACE_API_KEY = os.getenv('HUGGINGFACE_API_KEY')
API_URL = "https://api-inference.huggingface.co/models/CompVis/stable-diffusion-v1-4"

def generate_image(prompt):
    headers = {"Authorization": f"Bearer {HUGGINGFACE_API_KEY}"}
    data = {"inputs": prompt}
    response = requests.post(API_URL, headers=headers, json=data)

    if response.status_code == 200:
        return response.content  # Return image data
    else:
        raise Exception(f"Error: {response.status_code}, {response.text}")
