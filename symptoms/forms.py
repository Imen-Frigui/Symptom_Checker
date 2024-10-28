from django import forms
from .models import Symptom, Illness

class SymptomForm(forms.ModelForm):
    class Meta:
        model = Symptom
        fields = ['name', 'description']

class IllnessForm(forms.ModelForm):
    class Meta:
        model = Illness
        fields = ['name', 'description', 'symptoms']
