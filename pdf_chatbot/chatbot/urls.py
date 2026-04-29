from django.urls import path
from . import views

app_name = 'chatbot'

urlpatterns = [
    path('', views.home, name='home'),
    path('session/new/', views.new_session, name='new_session'),
    path('session/<int:session_id>/', views.session_view, name='session'),
    path('session/<int:session_id>/delete/', views.delete_session, name='delete_session'),
    path('api/upload-pdf/', views.upload_pdf, name='upload_pdf'),
    path('api/send-message/', views.send_message, name='send_message'),
    path('api/attach-document/', views.attach_document, name='attach_document'),
]
