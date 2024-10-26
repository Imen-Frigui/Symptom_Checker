from django.urls import path
from .views import (
    institution_list,
    create_institution,
    institution_detail,
    update_institution,
    delete_institution,
    institution_list_front,
    institution_detail_front
)

urlpatterns = [
    path('', institution_list, name='institution_list'),  # Lists all institutions
    path('new/', create_institution, name='create_institution'),  # Creates a new institution
    path('<int:pk>/', institution_detail, name='institution_detail'),  # Details of a specific institution
    path('<int:pk>/edit/', update_institution, name='update_institution'),  # Edit an institution
    path('<int:pk>/delete/', delete_institution, name='delete_institution'),  # Delete an institution
    path('front/', institution_list_front, name='institution_list_front'),  # Front office list of institutions
    path('front/<int:pk>/', institution_detail_front, name='institution_detail_front'),  # Correctly define the detail view with a pk
]   

