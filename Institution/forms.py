from django import forms
from .models import HealthCareInstitution

class HealthCareInstitutionForm(forms.ModelForm):
    class Meta:
        model = HealthCareInstitution
        fields = '__all__'  # Or list specific fields you want to include
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'institution_type': forms.Select(attrs={'class': 'form-control'}),
            'location': forms.Textarea(attrs={'class': 'form-control'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'website': forms.URLInput(attrs={'class': 'form-control'}),
            'operational_hours': forms.Textarea(attrs={'class': 'form-control'}),  # Consider JSON format
            'services_provided': forms.Textarea(attrs={'class': 'form-control'}),
            'insurance_accepted': forms.Textarea(attrs={'class': 'form-control'}),
            'rating': forms.NumberInput(attrs={'class': 'form-control', 'min': '1', 'max': '5'}),
            'capacity': forms.NumberInput(attrs={'class': 'form-control'}),
            'latitude': forms.NumberInput(attrs={'class': 'form-control'}),
            'longitude': forms.NumberInput(attrs={'class': 'form-control'}),
        }
