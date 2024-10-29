from django.urls import path
from . import views

app_name = 'documents'

urlpatterns = [
    path('', views.template_list, name='template_list'),
    path('create/', views.template_create, name='template_create'),
    path('edit/<int:pk>/', views.template_edit, name='template_edit'),
    path('invite/<int:template_id>/', views.invite_collaborator, name='invite_collaborator'),
]
