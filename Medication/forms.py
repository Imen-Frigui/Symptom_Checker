from django import forms
from .models import Medication
from .models import SideEffect
from .models import Treatment


class MedicationForm(forms.ModelForm):
    class Meta:
        model = Medication
        fields = ['name', 'description', 'image', 'side_effects']



class SideEffectForm(forms.ModelForm):
    class Meta:
        model = SideEffect
        fields = ['description']


class TreatmentForm(forms.ModelForm):
    class Meta:
        model = Treatment
        fields = ['name', 'description', 'medications']



