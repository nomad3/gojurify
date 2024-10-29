from django.urls import path
from . import views

app_name = 'documents'

urlpatterns = [
    path('', views.template_list, name='template_list'),
    path('create/', views.template_create, name='template_create'),
    path('edit/<int:pk>/', views.template_edit, name='template_edit'),
    path('invite/<int:pk>/', views.invite_collaborator, name='invite_collaborator'),
    path('export/pdf/<int:pk>/', views.export_pdf, name='export_pdf'),
    path('export/word/<int:pk>/', views.export_word, name='export_word'),
    path('export/google-docs/<int:pk>/', views.export_google_docs, name='export_google_docs'),
]
