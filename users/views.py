from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib import messages
from users.forms import SignUpForm
import logging
from django.contrib.auth.decorators import login_required
from .forms import ProfileForm
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.http import HttpResponse
from .huggingface_service import generate_image
import io
from users.forms import ImageGenerationForm
import os
from django.conf import settings
import time
import uuid
from os.path import basename
import shutil
from os.path import join, isfile
from django.contrib.auth import authenticate, login
import face_recognition
import cv2
import numpy as np
from .models import CustomUser
import cv2
import face_recognition
import numpy as np
from django.shortcuts import render, redirect
from .forms import SignUpForm
from django.shortcuts import get_object_or_404, redirect
from .forms import UserForm 
from transformers import pipeline
from .forms import SymptomForm

logger = logging.getLogger(__name__)

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('dashboard')
        else:
            logger.warning(f"Signup form is invalid: {form.errors}")
            messages.error(request, f"There was an error with your signup: {form.errors}")
    else:
        form = SignUpForm()

    return render(request, 'back_office/pages/sign-up.html', {'form': form})



@login_required
def profile(request):
    profile_form = ProfileForm(instance=request.user)
    password_form = PasswordChangeForm(request.user)
    image_generation_form = ImageGenerationForm()
    generated_image_url = None
    profile_picture_form = ProfilePictureForm(instance=request.user)

    return render(request, 'back_office/pages/profile.html', {
        'profile_form': profile_form,
        'password_form': password_form,
        'image_generation_form': image_generation_form,
        'generated_image_url': generated_image_url,
        'profile_picture_form': profile_picture_form,
    })


@login_required
def update_profile(request):
    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile has been updated successfully!')
            return redirect('profile')
    else:
        form = ProfileForm(instance=request.user)
    
    return render(request, 'back_office/pages/profile.html', {'profile_form': form})

@login_required
def change_password(request):
    if request.method == 'POST':
        password_form = PasswordChangeForm(request.user, request.POST)
        if password_form.is_valid():
            user = password_form.save()
            update_session_auth_hash(request, user)  # Keeps user logged in after password change
            messages.success(request, 'Your password was updated successfully!')
            return redirect('profile')
    else:
        password_form = PasswordChangeForm(request.user)

    return render(request, 'back_office/pages/profile.html', {'password_form': password_form})


@login_required
def generate_image_view(request):
    image_generation_form = ImageGenerationForm()
    generated_images = []

    # Define the directory where the images should be saved
    img_directory = os.path.join(settings.BASE_DIR, 'static', 'public', 'img')
    os.makedirs(img_directory, exist_ok=True)  # Ensure the directory exists

    # Generate a new image if the form is submitted
    if request.method == 'POST':
        description = request.POST.get('description')
        image_generation_form = ImageGenerationForm(request.POST)
        if description and image_generation_form.is_valid():
            try:
                # Call the Hugging Face API to generate the image
                image_data = generate_image(description)

                # Define the image path with a timestamp to make it unique
                timestamp = int(time.time())
                img_path = os.path.join(img_directory, f"{request.user.username}_generated_image_{timestamp}.png")
                
                # Save the image
                with open(img_path, 'wb') as img_file:
                    img_file.write(image_data)

                # Store the image data in the session for future access
                image_info = {
                    'url': f'/static/public/img/{os.path.basename(img_path)}',
                    'name': os.path.basename(img_path)
                }
                generated_images.append(image_info)

                # Ensure 'generated_images' exists in session
                if 'generated_images' not in request.session:
                    request.session['generated_images'] = []

                # Add the new image to session
                request.session['generated_images'].append(image_info)
                request.session.modified = True

                messages.success(request, 'Image generated and saved successfully!')
            except Exception as e:
                messages.error(request, f"Error generating image: {e}")

    # Retrieve previously generated images from session
    session_images = request.session.get('generated_images', [])

    # Retrieve all images from the static/public/img directory
    try:
        all_images = [f for f in os.listdir(img_directory) if os.path.isfile(os.path.join(img_directory, f))]
    except Exception as e:
        all_images = []
        messages.error(request, f"Error retrieving images from directory: {e}")

    # Convert image filenames to URLs for display
    all_image_urls = [f'/static/public/img/{img}' for img in all_images]

    # Render the profile page with all necessary context
    return render(request, 'back_office/pages/profile.html', {
        'image_generation_form': image_generation_form,
        'generated_images': session_images,  # Images from the session
        'all_image_urls': all_image_urls,  # All images in the static/public/img folder
        'profile_form': ProfileForm(instance=request.user),  # Pass the profile form
        'password_form': PasswordChangeForm(request.user),  # Pass the password form
    })


@login_required
def keep_img(request, image_name):
    """ Save the selected image as the profile picture for the user """
    img_directory = os.path.join(settings.MEDIA_ROOT, 'profile_pictures')
    os.makedirs(img_directory, exist_ok=True)

    img_source_path = os.path.join(settings.BASE_DIR, 'static', 'public', 'img', image_name)
    img_destination_path = os.path.join(img_directory, f"{request.user.username}_profile_picture.png")

    if os.path.exists(img_source_path):
        try:
            # If the destination file exists, remove it
            if os.path.exists(img_destination_path):
                os.remove(img_destination_path)

            # Copy the image from static to the media directory (keep it in both locations)
            shutil.copy(img_source_path, img_destination_path)

            # Update the user's profile picture field
            request.user.profile_picture = f'profile_pictures/{request.user.username}_profile_picture.png'
            request.user.save()
            messages.success(request, 'Profile picture updated successfully!')
        except Exception as e:
            messages.error(request, f"Error updating profile picture: {e}")
    else:
        messages.error(request, 'The selected image does not exist.')

    return redirect('profile')


from django.contrib import messages
from .forms import ProfilePictureForm

@login_required
def update_profile_picture(request):
    if request.method == 'POST':
        # Handle profile picture upload
        profile_picture_form = ProfilePictureForm(request.POST, request.FILES, instance=request.user)
        if profile_picture_form.is_valid():
            profile_picture_form.save()
            messages.success(request, 'Your profile picture has been uploaded successfully!')
            return redirect('profile')  # Redirect to the profile page
        else:
            messages.error(request, 'Error uploading profile picture. Please try again.')
    
    return redirect('profile')  # In case of a direct GET request, redirect to profile






from deepface import DeepFace
from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib import messages
from .models import CustomUser
import cv2
import os

def facial_login(request):
    if request.method == 'POST':
        # Capture an image from the camera
        video_capture = cv2.VideoCapture(0)
        ret, frame = video_capture.read()
        video_capture.release()

        if not ret:
            messages.error(request, "Failed to capture image from the camera.")
            return redirect('login')

        # Save the captured frame temporarily
        captured_img_path = "captured_img.jpg"
        cv2.imwrite(captured_img_path, frame)

        # Check against all users with profile pictures
        for user in CustomUser.objects.all():
            if user.profile_picture:
                try:
                    profile_picture_path = user.profile_picture.path
                    
                    # Compare the captured image with the user's profile picture using DeepFace
                    result = DeepFace.verify(img1_path=captured_img_path, img2_path=profile_picture_path)

                    if result["verified"]:
                        # Log the user in if the face matches
                        login(request, user)
                        messages.success(request, 'Logged in successfully using facial recognition!')
                        os.remove(captured_img_path)  # Clean up temporary image
                        return redirect('dashboard')
                except Exception as e:
                    print(f"Error processing user {user.username}: {e}")
                    continue  # If there's an issue, skip to the next user
        
        messages.error(request, 'No matching face found. Please try again.')
        return redirect('login')

    return render(request, 'back_office/pages/sign-in.html')

@login_required
def user_management(request):
    if request.user.role != 'admin':
        return redirect('dashboard')

    users = CustomUser.objects.all()
    return render(request, 'back_office/pages/users/user-management.html', {'users': users})

@login_required
def edit_user(request, user_id):
    if request.user.role != 'admin':  # Only admins can edit users
        return redirect('dashboard')

    user = get_object_or_404(CustomUser, id=user_id)

    if request.method == 'POST':
        form = UserForm(request.POST, instance=user)
        if form.is_valid():
            user = form.save(commit=False)
            
            # Check if both passwords are provided and match
            new_password = form.cleaned_data.get('new_password')
            confirm_password = form.cleaned_data.get('confirm_password')

            if new_password and confirm_password and new_password == confirm_password:
                user.set_password(new_password)
            
            user.save()  # Save the user with or without password update
            messages.success(request, 'User updated successfully!')
            return redirect('user_management')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = UserForm(instance=user)

    return render(request, 'back_office/pages/users/edit-user.html', {'form': form, 'user': user})




@login_required
def delete_user(request, user_id):
    if request.user.role != 'admin':
        return redirect('dashboard')

    user = get_object_or_404(CustomUser, id=user_id)

    if user.is_superuser:
        messages.error(request, "You cannot delete a superuser.")
        return redirect('user_management')

    user.delete()
    messages.success(request, "User deleted successfully.")
    return redirect('user_management')



# Load a pre-trained model from Hugging Face for symptom checking
# model = pipeline("text-generation", model="distilgpt2")
# # model = pipeline("text-generation", model="dmis-lab/biobert-base-cased-v1.1")
# def symptom_check(request):
#     result = None
#     if request.method == 'POST':
#         form = SymptomForm(request.POST)
#         if form.is_valid():
#             symptoms = form.cleaned_data['symptoms']
#             prompt = f"The patient has the following symptoms: {symptoms}. What could be the possible diagnosis?"
#             result = model(prompt)[0]['generated_text']
#             # result = model(prompt, max_length=100, max_new_tokens=50)[0]['generated_text']
#     else:
#         form = SymptomForm()
    
#     return render(request, 'symptom_checker.html', {'form': form, 'result': result})

from transformers import pipeline

# Load a question-answering model instead of text generation
model = pipeline("question-answering")

@login_required
def symptom_check(request):
    result = None
    if request.method == 'POST':
        form = SymptomForm(request.POST)
        if form.is_valid():
            symptoms = form.cleaned_data['symptoms']
            prompt = f"What are the possible diagnoses for these symptoms: {symptoms}?"
            
            # Provide context for the question-answering model
            context = "This patient reports having fever, headache, and cough. Common diagnoses include viral infections, colds, and flu."

            # Use question-answering model instead of text generation
            result = model(question=prompt, context=context)['answer']
    else:
        form = SymptomForm()

    return render(request, 'back_office/pages/dashboard.html', {'form': form, 'result': result})
