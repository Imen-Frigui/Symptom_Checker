from django.contrib import admin
from django.urls import include, path, include
from symptom_checker_application import views
from django.conf import settings
from django.conf.urls.static import static



urlpatterns = [
    path('admin/', admin.site.urls),
    #  path('', include('symptom_checker_application.urls')), 
    path('', views.index, name='index'),  # This is your main index page
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('blog/', views.blog, name='blog'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('symptoms/', include('symptoms.urls')),
    path('medication/', include('Medication.urls')), 
    
    # Back office URLs
    path('institution/', include('Institution.urls')),  # Includes your back office URLs
    path('consultation/', include('Consultation.urls')),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
