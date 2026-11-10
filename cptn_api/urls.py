from django.contrib import admin
from django.urls import path, include
from django.http import JsonResponse
from django.utils import timezone

# A simple health check function-based view
def health_check(request):
    """
    Returns the system status and current server time.
    Useful for monitoring and Docker health checks.
    """
    data = {
        "status": "healthy",
        "timestamp": timezone.now(),
        "service": "CPTN API",
        "version": "v1.0.0"
    }
    return JsonResponse(data)

urlpatterns = [
    # 1. Health Check (Root or /health/)
    path('health/', health_check, name='health_check'),

    # 2. Django Admin Interface
    path('admin/', admin.site.urls),

    # 3. CPTN API VERSION 1
    # Base: /api/v1/journey/
    path('api/v1/journey/', include('journey.urls')),

    # 4. AUTHENTICATION
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]