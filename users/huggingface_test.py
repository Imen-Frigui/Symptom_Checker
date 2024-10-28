import os
import requests
from dotenv import load_dotenv
import base64

# Load environment variables from .env
load_dotenv()

HUGGINGFACE_API_KEY = os.getenv('HUGGINGFACE_API_KEY')
API_URL = "https://api-inference.huggingface.co/models/CompVis/stable-diffusion-v1-4"

def generate_image(prompt):
    headers = {"Authorization": f"Bearer {HUGGINGFACE_API_KEY}"}
    data = {"inputs": prompt}
    response = requests.post(API_URL, headers=headers, json=data)

    if response.status_code == 200:
        print("Image generated successfully!")
        # Write the binary image to a file to check if it's working
        with open("generated_image.png", "wb") as f:
            f.write(response.content)
        print("Image saved as 'generated_image.png'")
    else:
        print(f"Error: {response.status_code}, {response.text}")

if __name__ == "__main__":
    prompt = "A futuristic city with flying cars"
    generate_image(prompt)
