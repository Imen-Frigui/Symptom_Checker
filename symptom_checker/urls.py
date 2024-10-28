from django.contrib import admin
from django.urls import path, include
from symptom_checker_application import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),  # This is your main index page
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('blog/', views.blog, name='blog'),
    path('dashboard/', views.dashboard, name='dashboard'),
    
    # Back office URLs
    path('institution/', include('Institution.urls')),  # Includes your back office URLs
    path('consultation/', include('Consultation.urls')),

]
