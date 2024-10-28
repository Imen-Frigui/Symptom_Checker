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

class ProfilePictureForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['profile_picture']

class UserForm(forms.ModelForm):
    new_password = forms.CharField(widget=forms.PasswordInput(), required=False)
    confirm_password = forms.CharField(widget=forms.PasswordInput(), required=False)

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'first_name', 'last_name', 'role']

    def clean(self):
        cleaned_data = super().clean()
        new_password = cleaned_data.get("new_password")
        confirm_password = cleaned_data.get("confirm_password")

        if new_password and new_password != confirm_password:
            self.add_error('confirm_password', "Passwords do not match")

        return cleaned_data

class SymptomForm(forms.Form):
    symptoms = forms.CharField(
        label='Symptoms',
        widget=forms.Textarea(attrs={"placeholder": "Enter symptoms, e.g., fever, cough, fatigue"})
    )

