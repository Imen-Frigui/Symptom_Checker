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

    return render(request, 'back_office/pages/profile.html', {
        'profile_form': profile_form,
        'password_form': password_form,
        'image_generation_form': image_generation_form,
        'generated_image_url': generated_image_url,
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


def capture_and_encode_face(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()

            # Capture the user's face using OpenCV
            video_capture = cv2.VideoCapture(0)

            ret, frame = video_capture.read()
            video_capture.release()

            # Convert the image from BGR color (which OpenCV uses) to RGB color
            rgb_frame = frame[:, :, ::-1]

            # Find all the faces in the image
            face_locations = face_recognition.face_locations(rgb_frame)
            if face_locations:
                # Get the encoding of the first face
                face_encoding = face_recognition.face_encodings(rgb_frame, face_locations)[0]

                # Store the face encoding in the user's profile
                user.face_encoding = np.array2string(face_encoding)
                user.save()
                messages.success(request, 'Your face has been registered successfully!')

                return redirect('login')
            else:
                messages.error(request, 'No face detected. Please try again.')

    else:
        form = SignUpForm()

    return render(request, 'users/register.html', {'form': form})

def facial_login(request):
    if request.method == 'POST':
        # Capture the user's face using OpenCV
        video_capture = cv2.VideoCapture(0)

        ret, frame = video_capture.read()
        video_capture.release()

        # Convert the image from BGR color to RGB color
        rgb_frame = frame[:, :, ::-1]

        # Find all the faces in the image
        face_locations = face_recognition.face_locations(rgb_frame)
        if face_locations:
            # Get the encoding of the captured face
            face_encoding = face_recognition.face_encodings(rgb_frame, face_locations)[0]

            # Iterate over all users and compare the face encoding
            users = CustomUser.objects.all()
            for user in users:
                if user.face_encoding:
                    # Load the saved face encoding
                    saved_face_encoding = np.fromstring(user.face_encoding[1:-1], sep=' ')

                    # Compare the captured face encoding with the saved face encoding
                    matches = face_recognition.compare_faces([saved_face_encoding], face_encoding)

                    if matches[0]:
                        # Log in the user if there is a match
                        login(request, user)
                        messages.success(request, 'Logged in successfully using facial recognition!')
                        return redirect('dashboard')

            messages.error(request, 'No matching face found. Please try again.')

    return render(request, 'users/facial_login.html')