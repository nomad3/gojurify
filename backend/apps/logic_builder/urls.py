from django.urls import path
from . import views

app_name = 'logic_builder'

urlpatterns = [
    path('<int:template_id>/', views.logic_builder_view, name='logic_builder'),
]
