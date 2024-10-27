# models.py

from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
from decimal import Decimal  # Add this import at the top of your models.py

class HealthCareInstitution(models.Model):
    INSTITUTION_TYPES = [
        ('hospital', 'Hospital'),
        ('clinic', 'Clinic'),
        ('pharmacy', 'Pharmacy'),
        ('diagnostic_center', 'Diagnostic Center'),
    ]

    name = models.CharField(max_length=255)
    institution_type = models.CharField(max_length=50, choices=INSTITUTION_TYPES)
    location = models.TextField()
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    website = models.URLField(blank=True, null=True)
    operational_hours = models.JSONField(blank=True, null=True)
    services_provided = models.TextField(blank=True)
    insurance_accepted = models.TextField(blank=True, null=True)
    rating = models.DecimalField(
        max_digits=3,
        decimal_places=2,
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        blank=True,
        null=True
    )
    capacity = models.IntegerField(blank=True, null=True)
    latitude = models.DecimalField(max_digits=20, decimal_places=6, blank=True, null=True)
    longitude = models.DecimalField(max_digits=20, decimal_places=6, blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Health Care Institutions"

class HealthcareRecommender:
    def __init__(self, institutions):
        # Convert queryset to DataFrame for easier manipulation
        self.institutions = pd.DataFrame(list(institutions.values()))
        print("Institutions DataFrame:", self.institutions)  # Debugging line

    def fit_model(self):
        # Prepare data for clustering
        data = self.institutions[['latitude', 'longitude', 'rating']].dropna()
        
        if data.empty:
            print("No data available for clustering.")  # Debugging line
            return
        
        # Fit KMeans clustering
        kmeans = KMeans(n_clusters=5)  # Example: 5 clusters
        self.institutions['cluster'] = kmeans.fit_predict(data[['latitude', 'longitude', 'rating']])
        self.model = kmeans
        print("Clusters assigned to institutions:", self.institutions['cluster'].unique())  # Debugging line

    def recommend(self, user_location, num_recommendations=3):
        # Calculate distances to the user's location
        user_lat, user_lon = user_location
        
        self.institutions['distance'] = self.institutions.apply(
            lambda row: np.sqrt((row['latitude'] - user_lat) ** 2 + (row['longitude'] - user_lon) ** 2), axis=1
        )

        print("Distances calculated:", self.institutions['distance'])  # Debugging line
        
        # Get the nearest institutions based on distance
        recommendations = self.institutions.nsmallest(num_recommendations, 'distance')
        print("Recommendations:", recommendations)  # Debugging line
        return recommendations
