from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from .views import health_check

# API documentation schema
schema_view = get_schema_view(
    openapi.Info(
        title="Document Management API",
        default_version='v1',
        description="API documentation for Document Management System",
        terms_of_service="https://www.example.com/terms/",
        contact=openapi.Contact(email="contact@example.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    # Admin
    path('admin/', admin.site.urls),
    
    # API Documentation
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0),
         name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0),
         name='schema-redoc'),
    
    # Health Check
    path('health/', health_check, name='health_check'),
    
    # Authentication
    path('api/token/', TokenObtainPairView.as_view(),
         name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(),
         name='token_refresh'),
    
    # Apps
    path('users/', include('apps.users.urls', namespace='users')),
    path('documents/', include('apps.documents.urls', namespace='documents')),
    path('intake/', include('apps.intake.urls', namespace='intake')),
    path('logic-builder/', include('apps.logic_builder.urls',
         namespace='logic_builder')),
    path('api/', include('apps.api.urls', namespace='api')),
]

# Serve static/media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                         document_root=settings.MEDIA_ROOT)
    urlpatterns += staticfiles_urlpatterns()
