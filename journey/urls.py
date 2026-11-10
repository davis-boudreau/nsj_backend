from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    AreaViewSet,
    StopViewSet,
    AvailableTripViewSet, 
    RideRequestViewSet, 
    AgencyViewSet,
    OfferCreateView,
    check_auth,
    get_route_preview
)

# 1. Initialize the Router. This will automatically generate URL patterns for our ViewSets.
router = DefaultRouter()

# 2. Register ViewSets
# These will be appended to the versioned prefix defined in the project urls.py
router.register(r'areas', AreaViewSet, basename='area')
router.register(r'stops', StopViewSet, basename='stop')
router.register(r'trips', AvailableTripViewSet, basename='trip')
router.register(r'requests', RideRequestViewSet, basename='request')
router.register(r'agencies', AgencyViewSet, basename='agency')

# 3. Define URL Patterns.  Class `OfferCreateView` is a custom endpoint for creating offers, so we add it separately.
urlpatterns = [
    path('', include(router.urls)),
    # Specific POST endpoint for Phase 1
    path('offer/', OfferCreateView.as_view(), name='offer-create'),
    
    # Changed from 'auth-check/' to 'check-auth/' to match JS fetch.  Function name remains `check_auth` for clarity.
    path('check-auth/', check_auth, name='check-auth'),

    # New endpoint for route preview
    path('get-route/', get_route_preview, name='get-route-preview'),  
]