from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class CustomUser(AbstractUser):
    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('simple', 'Simple'),
    ]

    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)
    address = models.TextField(blank=True)
    phone = models.CharField(max_length=15, blank=True)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='simple')
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)
    # To store the face encoding
    face_encoding = models.TextField(null=True, blank=True)  

    # We can customize or override methods if necessary

    def __str__(self):
        return self.username
