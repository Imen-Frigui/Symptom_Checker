# health_service.py
import requests
import hashlib
import hmac
import base64

class PriaidHealthService:
    def __init__(self, api_key, secret_key, auth_url, language, health_service_url):
        self.api_key = api_key
        self.secret_key = secret_key
        self.auth_url = auth_url
        self.language = language
        self.health_service_url = health_service_url
        self.token = self.authenticate()

    def authenticate(self):
        try:
            # Construct the URL with format=json
            uri = f"{self.auth_url}?format=json"
            
            # Create HMACMD5 hash of the URI using the secret key
            secret_bytes = self.secret_key.encode('utf-8')
            data_bytes = uri.encode('utf-8')
            computed_hash = hmac.new(secret_bytes, data_bytes, hashlib.md5).digest()
            computed_hash_string = base64.b64encode(computed_hash).decode('utf-8')
            
            # Create the Authorization header
            authorization_header = f"Bearer {self.api_key}:{computed_hash_string}"
            
            # Make the POST request to get the access token
            headers = {
                "Authorization": authorization_header
            }
            
            response = requests.post(uri, headers=headers)
            
            # Check if the response is successful
            if response.status_code == 200:
                token_info = response.json()
                return token_info.get("Token")
            else:
                # If the response failed, raise an exception
                raise Exception(f"Authentication failed. HTTP Status Code: {response.status_code}. Error: {response.json().get('message', 'Unknown error')}")
        
        except Exception as e:
            raise Exception(f"Error during authentication: {e}")

    def get_symptoms(self):
        url = f"{self.health_service_url}/symptoms?token={self.token}&language={self.language}"
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception("Failed to fetch symptoms.")

    def get_diagnosis(self, symptoms, gender, year_of_birth):
        url = f"{self.health_service_url}/diagnosis?token={self.token}&language={self.language}&symptoms={symptoms}&gender={gender}&year_of_birth={year_of_birth}"
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception("Failed to fetch diagnosis.")
