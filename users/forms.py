from django import forms
from django.contrib.auth.forms import UserCreationForm
from users.models import CustomUser

class SignUpForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password1', 'password2']

class ProfileForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'first_name', 'last_name', 'email', 'address', 'phone']

class ImageGenerationForm(forms.Form):
    description = forms.CharField(max_length=255, widget=forms.Textarea(attrs={
        'class': 'form-control',
        'placeholder': 'Enter a description for the image...',
        'rows': 3,
    }))