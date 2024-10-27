import requests
import hmac
import hashlib
import base64
import os
from decouple import config

class PriaidHealthService:
    def __init__(self, api_key, secret_key, auth_url, language, health_service_url):
        self.api_key = api_key
        self.secret_key = secret_key
        self.auth_url = auth_url
        self.language = language
        self.health_service_url = health_service_url
        self.token = self.authenticate()

    def authenticate(self):
        # Create HMACMD5 hash
        uri = self.auth_url
        hashed_credentials = self.generate_hmac_md5_hash(uri, self.secret_key)

        headers = {
            'Authorization': f'Bearer {self.api_key}:{hashed_credentials}'
        }

        response = requests.post(uri, headers=headers)
        if response.status_code == 200:
            return response.json()['Token']
        else:
            raise Exception("Authentication failed. Please check your credentials.")

    def generate_hmac_md5_hash(self, uri, secret_key):
        secret_bytes = bytes(secret_key, 'utf-8')
        uri_bytes = bytes(uri, 'utf-8')
        hmac_hash = hmac.new(secret_bytes, uri_bytes, hashlib.md5)
        return base64.b64encode(hmac_hash.digest()).decode()

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
