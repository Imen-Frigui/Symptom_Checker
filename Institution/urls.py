from django.urls import path
from .views import (
    institution_list,
    create_institution,
    institution_detail,
    update_institution,
    delete_institution,
    institution_list_front,
    institution_detail_front,
    find_nearby_institutions,
    recommend_institution,
    chatbot_view,
    chatbot_reply,
    open_chatbot
    
)

urlpatterns = [
    path('', institution_list, name='institution_list'),  # Lists all institutions
    path('new/', create_institution, name='create_institution'),  # Creates a new institution
    path('<int:pk>/', institution_detail, name='institution_detail'),  # Details of a specific institution
    path('<int:pk>/edit/', update_institution, name='update_institution'),  # Edit an institution
    path('<int:pk>/delete/', delete_institution, name='delete_institution'),  # Delete an institution
    path('front/', institution_list_front, name='institution_list_front'),  # Front office list of institutions
    path('front/<int:pk>/', institution_detail_front, name='institution_detail_front'),  # Correctly define the detail view with a pk
    path('find-nearby/', find_nearby_institutions, name='find_nearby_institutions'),
     path('recommend/', recommend_institution, name='recommend_institution'),
    path('chatbot/', chatbot_view, name='chatbot_view'),
    path('chatbot/reply/', chatbot_reply, name='chatbot_reply'),
path('open_chatbot/', open_chatbot, name='open_chatbot'),

    ]   

