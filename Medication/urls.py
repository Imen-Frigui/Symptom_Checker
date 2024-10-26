from django.urls import path
from . import views

urlpatterns = [
    # Medications URLs
    path('medications/', views.medication_list, name='medication_list'),
    path('medications/<int:pk>/', views.medication_detail, name='medication_detail'),
    path('medications/create/', views.medication_create, name='medication_create'),
    path('medications/<int:pk>/update/', views.medication_update, name='medication_update'),
    path('medications/<int:pk>/delete/', views.medication_delete, name='medication_delete'),

    # Side Effects URLs
    path('side-effects/', views.sideeffect_list, name='sideeffect_list'),
    path('side-effects/create/', views.sideeffect_create, name='sideeffect_create'),
    path('side-effects/<int:pk>/update/', views.sideeffect_update, name='sideeffect_update'),
    path('side-effects/<int:pk>/delete/', views.sideeffect_delete, name='sideeffect_delete'),

    # Treatments URLs
    path('treatments/<int:pk>/', views.treatment_detail, name='treatment_detail'),
    path('treatments/', views.treatment_list, name='treatment_list'),
    path('treatments/create/', views.treatment_create, name='treatment_create'),
    path('treatments/<int:pk>/update/', views.treatment_update, name='treatment_update'),
    path('treatments/<int:pk>/delete/', views.treatment_delete, name='treatment_delete'),

   
]
