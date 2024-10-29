import time
import logging
from django.conf import settings
from django.http import JsonResponse
from django.urls import resolve

logger = logging.getLogger(__name__)

class RequestLoggingMiddleware:
    """Log all requests and their processing time."""
    
    def __init__(self, get_response):
        self.get_response = get_response
        
    def __call__(self, request):
        # Start timer
        start_time = time.time()
        
        # Get the current route
        route = resolve(request.path_info).url_name
        
        # Process the request
        response = self.get_response(request)
        
        # Calculate request processing time
        duration = time.time() - start_time
        
        # Log request details
        logger.info(
            f"Method: {request.method} | "
            f"Path: {request.path} | "
            f"Route: {route} | "
            f"Status: {response.status_code} | "
            f"Duration: {duration:.2f}s | "
            f"User: {request.user}"
        )
        
        return response

class PerformanceMonitoringMiddleware:
    """Monitor request performance and alert on slow requests."""
    
    def __init__(self, get_response):
        self.get_response = get_response
        self.slow_request_threshold = getattr(settings,
                                            'SLOW_REQUEST_THRESHOLD', 1.0)
        
    def __call__(self, request):
        start_time = time.time()
        response = self.get_response(request)
        duration = time.time() - start_time
        
        if duration > self.slow_request_threshold:
            logger.warning(
                f"Slow request detected: {request.path} "
                f"took {duration:.2f}s to process"
            )
            
        return response

class ErrorHandlingMiddleware:
    """Handle exceptions and provide appropriate responses."""
    
    def __init__(self, get_response):
        self.get_response = get_response
        
    def __call__(self, request):
        return self.get_response(request)
        
    def process_exception(self, request, exception):
        # Log the error
        logger.error(f"Error processing request: {str(exception)}",
                    exc_info=True)
        
        # Check if request expects JSON
        if request.headers.get('Accept') == 'application/json':
            return JsonResponse({
                'error': 'Internal Server Error',
                'detail': str(exception) if settings.DEBUG else 'An error occurred'
            }, status=500)
        
        # Let Django's default error handling take care of other cases
        return None 