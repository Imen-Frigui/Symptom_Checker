from django.urls import path
from django.urls import path, include  # Import 'include' for including app URLs

from .views import (
    institution_list,
    create_institution,
    institution_detail,
    update_institution,
    delete_institution,  # Ensure this matches your delete view
)

urlpatterns = [
    path('', institution_list, name='institution_list'),  # Lists all institutions
    path('new/', create_institution, name='create_institution'),  # Creates a new institution
    path('<int:pk>/', institution_detail, name='institution_detail'),  # Details of a specific institution
    path('<int:pk>/edit/', update_institution, name='update_institution'),  # Edit an institution
    path('<int:pk>/delete/', delete_institution, name='delete_institution'),  # Changed to use 'pk'
]
