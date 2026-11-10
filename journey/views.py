import requests, json
from django.conf import settings
from django.db import models
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Case, When, Value, IntegerField
from rest_framework import viewsets, filters, status, generics, permissions
from rest_framework.response import Response
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from django.contrib.gis.geos import Point, GEOSGeometry, LineString
from django.contrib.gis.measure import D
from .models import Trips, Stops, Area, CPTNRideRequest, Agency
from .serializers import (TripSerializer, StopSerializer, AreaSerializer, RideRequestSerializer, AgencySerializer, OfferSerializer)
from .pagination import StandardResultsPagination

# ==========================================
# SECTION 1: SEARCH & SELECTION
# ==========================================

class AreaViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = AreaSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['area_id', 'area_name', 'county', 'location_narrative']
    pagination_class = StandardResultsPagination

    def get_queryset(self):
        query = self.request.query_params.get('search', None)
        # Base queryset with optimization
        qs = Area.objects.prefetch_related('stops').all()

        if query:
            # Combined Filtering + Relevance Scoring
            # We use icontains to match the SearchFilter behavior but add scoring
            qs = qs.filter(
                models.Q(area_name__icontains=query) | 
                models.Q(county__icontains=query)
            ).annotate(
                relevance=Case(
                    When(area_name__iexact=query, then=Value(1)),
                    When(area_name__istartswith=query, then=Value(2)),
                    default=Value(3),
                    output_field=IntegerField(),
                )
            ).order_by('relevance', 'area_name')
        else:
            qs = qs.order_by('area_name')
        return qs

class StopViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = StopSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['stop_id', 'stop_code', 'stop_name', 'stop_desc']
    pagination_class = StandardResultsPagination

    def get_queryset(self):
        query = self.request.query_params.get('search', None)
        qs = Stops.objects.prefetch_related('areas').all()

        if query:
            qs = qs.filter(
                models.Q(stop_name__icontains=query) | 
                models.Q(stop_desc__icontains=query)
            ).annotate(
                relevance=Case(
                    When(stop_name__iexact=query, then=Value(1)),
                    When(stop_name__istartswith=query, then=Value(2)),
                    default=Value(3),
                    output_field=IntegerField(),
                )
            ).order_by('relevance', 'stop_name')
        else:
            qs = qs.order_by('stop_name')
        return qs

    @action(detail=False, methods=['get'])
    def nearby(self, request):
        lat = request.query_params.get('lat')
        lon = request.query_params.get('lon')
        dist_m = request.query_params.get('dist', 500)

        if not lat or not lon:
            return Response(
                {"error": "Provide 'lat' and 'lon' parameters."},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            user_location = Point(float(lon), float(lat), srid=4326)
            stops = Stops.objects.filter(
                location__distance_lte=(user_location, D(m=float(dist_m)))
            )
            serializer = self.get_serializer(stops, many=True)
            return Response(serializer.data)
        except ValueError:
            return Response(
                {"error": "Invalid lat/lon format."},
                status=status.HTTP_400_BAD_REQUEST
            )


# ==========================================
# SECTION 2: TRIPS
# ==========================================

class AvailableTripViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = TripSerializer

    def get_queryset(self):
        queryset = Trips.objects.all()
        route_name = self.request.query_params.get('route_name')
        if route_name:
            queryset = queryset.filter(route__route_short_name__icontains=route_name)
        return queryset


# ==========================================
# SECTION 3: TRANSACTIONAL & PROVIDERS
# ==========================================

class OfferCreateView(generics.CreateAPIView):
    """
    POST /api/v1/journey/offer/
    """
    serializer_class = OfferSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save()


class RideRequestViewSet(viewsets.ModelViewSet):
    queryset = CPTNRideRequest.objects.all()
    serializer_class = RideRequestSerializer

    def perform_create(self, serializer):
        serializer.save(rider=self.request.user)

    @action(detail=True, methods=['post'])
    def accept(self, request, pk=None):
        ride_request = self.get_object()
        ride_request.status = 'Accepted'
        ride_request.save()
        return Response({'status': 'Ride Accepted'})


class AgencyViewSet(viewsets.ModelViewSet):
    queryset = Agency.objects.all()
    serializer_class = AgencySerializer


# ==========================================
# SECTION 4: AUTH CHECK
# ==========================================

@csrf_exempt
@api_view(['GET'])
def check_auth(request):
    if not request.user.is_authenticated:
        return Response({"error": "Not authenticated"}, status=403)

    profile = getattr(request.user, 'profile', None)
    return Response({
        "isAuthenticated": True,
        "username": request.user.username,
        "is_driver": getattr(profile, 'is_driver', False)
    })

# ==========================================
# SECTION 5: ORS API
# ==========================================

@api_view(['POST'])
@permission_classes([IsAuthenticated])

def get_route_preview(request):
    start = request.data.get('start')
    end = request.data.get('end')

    if not start or not end:
        return Response({"error": "Start and End coordinates required"}, status=status.HTTP_400_BAD_REQUEST)

    ors_url = "https://api.openrouteservice.org/v2/directions/driving-car/geojson"
    headers = {
        'Authorization': settings.ORS_API_KEY,
        'Content-Type': 'application/json'
    }
    
    body = {
        "coordinates": [start, end],
        "instructions": False,
        "preference": "shortest",
        "alternative_routes": {
            "target_count": 3,
            "weight_factor": 1.5,
            "share_factor": 0.85,
        }
    }

    try:
        response = requests.post(ors_url, json=body, headers=headers)
        
        if response.status_code != 200:
            error_detail = response.json().get('error', {}).get('message', 'Unknown ORS error')
            if response.status_code == 400:
                del body["alternative_routes"]
                response = requests.post(ors_url, json=body, headers=headers)
                response.raise_for_status()
            else:
                return Response({"error": error_detail}, status=response.status_code)

        data = response.json()
        routes = []
        all_route_geometries = []

        for index, feature in enumerate(data.get('features', [])):
            geom_data = feature['geometry']
            routes.append({
                "geometry": geom_data,
                "summary": feature['properties'].get('summary', {}),
                "is_primary": index == 0
            })
            
            # Use json.dumps for clean conversion to GEOS
            # Explicitly set SRID to 4326 (standard for GeoJSON/GPS)
            geos_geom = GEOSGeometry(json.dumps(geom_data), srid=4326)
            all_route_geometries.append(geos_geom)

        stops_data = []
        if all_route_geometries:
            # Combine routes into one "search area"
            combined_routes = all_route_geometries[0]
            for g in all_route_geometries[1:]:
                combined_routes = combined_routes.union(g)

            # Spatial Query: location__distance_lte uses meters if SRID is 4326
            # Note: Ensure your model field is named 'location' and is a PointField with srid=4326
            nearby_stops = Stops.objects.filter(
                location__distance_lte=(combined_routes, D(m=450)) 
            ).distinct()

            for stop in nearby_stops:
                stops_data.append({
                "id": stop.stop_id,
                "name": stop.stop_name,
                "lat": stop.location.y,
                "lng": stop.location.x,
                "icon_filename": stop.stop_icon,  # Sending the filename from the DB
                "desc": stop.stop_desc
            })

        return Response({
            "routes": routes,
            "stops": stops_data
        })

    except Exception as e:
        print(f"Server-side Exception: {str(e)}")
        return Response({"error": str(e)}, status=status.HTTP_502_BAD_GATEWAY)