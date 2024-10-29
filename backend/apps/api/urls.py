from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import DocumentTemplateViewSet

router = DefaultRouter()
router.register(r'document-templates', DocumentTemplateViewSet, basename='document-template')

app_name = 'api'

urlpatterns = [
    path('', include(router.urls)),
]
