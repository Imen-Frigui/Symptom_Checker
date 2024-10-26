"""
URL configuration for symptom_checker project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from symptom_checker_application import views
from django.contrib.auth import views as auth_views
from users import views as user_views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),	
    path('contact/', views.contact, name='contact'),
    path('blog/', views.blog, name='blog'),
    path('dashboard/', views.dashboard, name='dashboard'),

    # Authentication
    path('accounts/login/', auth_views.LoginView.as_view(template_name='back_office/pages/sign-in.html'), name='login'),
    path('accounts/logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('signup/', user_views.signup, name='signup'),

    # User Management
    path('profile/', user_views.profile, name='profile'),
    path('profile/update/', user_views.update_profile, name='update_profile'),
    path('profile/change-password/', user_views.change_password, name='change_password'), 

    #User Ai
    path('profile/generate-image/', user_views.generate_image_view, name='generate_image'),
    path('profile/keep-image/<str:image_name>/', user_views.keep_img, name='keep_image'),
    
    # Facial recognition routes
    path('register/', user_views.capture_and_encode_face, name='register'),
    path('login/', user_views.facial_login, name='facial_login'),

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)