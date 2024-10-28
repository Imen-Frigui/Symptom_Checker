from django.urls import path
from . import views
from .views import MedicalEntityView
urlpatterns = [
    # Route for listing symptoms from the local database
    path('', views.list_local_symptoms, name='list_local_symptoms'),

    # Route for adding a new symptom
    path('add/', views.add_symptom, name='add_symptom'),

    # Route for updating an existing symptom
    path('update/<int:pk>/', views.update_symptom, name='update_symptom'),

    # Route for deleting an existing symptom
    path('delete/<int:pk>/', views.delete_symptom, name='delete_symptom'),

    # Route for diagnosing based on selected symptoms
    path('diagnose/', views.diagnose, name='diagnose'),

    # Route for fetching symptoms from the health service (optional)
    path('external-symptoms/', views.list_external_symptoms, name='list_external_symptoms'),
    path('medical-entities/', MedicalEntityView.as_view(), name='medical_entities'),
]
