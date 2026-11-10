import uuid
import openrouteservice
from django.conf import settings
from django.templatetags.static import static
from django.conf import settings
from datetime import timedelta
from django.db import transaction
from rest_framework import serializers
from rest_framework_gis.serializers import GeoFeatureModelSerializer
from django.contrib.auth.models import User
from django.contrib.gis.geos import LineString, Point
from .models import (
    Agency, Routes, Trips, StopTimes, Stops, Frequencies, 
    Area, Calendar, CPTNUserProfile,
    CPTNTripCapacity, CPTNRideRequest, Shapes
)

# ==========================================
# SECTION 1: IDENTITY & PROFILE
# ==========================================

class UserProfileSerializer(serializers.ModelSerializer):
    agency_name = serializers.ReadOnlyField(source='agency.agency_name')

    class Meta:
        model = CPTNUserProfile
        fields = ['is_driver', 'is_rider', 'vehicle_desc', 'default_seats', 'agency', 'agency_name']

class UserSerializer(serializers.ModelSerializer):
    profile = UserProfileSerializer(read_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'profile']

# ==========================================
# SECTION 2: SPATIAL & INFRASTRUCTURE
# ==========================================

class ShapeSerializer(serializers.ModelSerializer):
    """
    Serializes the Shape and its LineString geometry.
    Ensures geometry is returned as GeoJSON for Leaflet.
    """
    class Meta:
        model = Shapes
        fields = ['shape_id', 'geometry']

class AreaSerializer(GeoFeatureModelSerializer):
    class Meta:
        model = Area
        geo_field = "location"
        id_field = "area_id"
        fields = ['area_id', 'area_name', 'county', 'location_narrative']


class StopSerializer(GeoFeatureModelSerializer):
    areas = AreaSerializer(many=True, read_only=True)
    # New field to provide the full path to the icon asset
    stop_icon_url = serializers.SerializerMethodField()

    class Meta:
        model = Stops
        geo_field = "location"
        id_field = "stop_id"
        fields = [
            'stop_id', 'stop_code', 'stop_name', 'stop_desc', 
            'stop_icon', 'stop_icon_url', 'location_type', 'areas'
        ]

    def get_stop_icon_url(self, obj):
        if obj.stop_icon:
            # This points to your static folder, e.g., static/icons/pin.png
            return static(f"icons/{obj.stop_icon}")
        return None
            
class StopTimeSerializer(serializers.ModelSerializer):
    stop_name = serializers.ReadOnlyField(source='stop.stop_name')
    stop_details = StopSerializer(source='stop', read_only=True)
    
    class Meta:
        model = StopTimes
        fields = [
            'stop_sequence', 'stop', 'stop_name', 'stop_details',
            'arrival_time', 'departure_time', 'pickup_type'
        ]

# ==========================================
# SECTION 3: JOURNEY ENGINE (NESTED DATA)
# ==========================================

class AgencySerializer(serializers.ModelSerializer):
    class Meta:
        model = Agency
        fields = '__all__'

class TripCapacitySerializer(serializers.ModelSerializer):
    class Meta:
        model = CPTNTripCapacity
        fields = ['total_seats', 'available_seats']

class TripSerializer(serializers.ModelSerializer):
    """
    Main Trip Serializer.
    Nests 'shape' for immediate map rendering after POST.
    """
    stop_times = StopTimeSerializer(many=True, read_only=True)
    capacity = TripCapacitySerializer(source='cptntripcapacity', read_only=True)
    shape = ShapeSerializer(read_only=True)
    route_name = serializers.ReadOnlyField(source='route.route_short_name')
    driver_agency = serializers.ReadOnlyField(source='route.agency.agency_name')

    class Meta:
        model = Trips
        fields = [
            'trip_id', 'route', 'route_name', 'driver_agency', 
            'service_id', 'shape', 'trip_headsign', 
            'stop_times', 'capacity', 'created_at'
        ]

# ==========================================
# SECTION 4: PHASE 1 OFFER LOGIC
# ==========================================

class OfferSerializer(serializers.Serializer):
    # Core Route Data
    origin_area_id = serializers.CharField()
    destination_stop_id = serializers.CharField()
    
    # Temporal Logic (Calendar)
    start_date = serializers.DateField()
    end_date = serializers.DateField()
    days_of_week = serializers.ListField(
        child=serializers.ChoiceField(choices=[
            'monday', 'tuesday', 'wednesday', 'thursday', 
            'friday', 'saturday', 'sunday'
        ])
    )
    
    # Timing & Frequency
    departure_time = serializers.TimeField()
    end_time = serializers.TimeField(required=False, allow_null=True)
    headway_minutes = serializers.IntegerField(required=False, min_value=1)
    
    # Capacity
    available_seats = serializers.IntegerField(min_value=1)

    def create(self, validated_data):
        user = self.context['request'].user
        days = validated_data['days_of_week']
        
        # 1. Fetch Location Objects
        origin = Area.objects.get(area_id=validated_data['origin_area_id'])
        destination = Stops.objects.get(stop_id=validated_data['destination_stop_id'])

        with transaction.atomic():
            # 2. IDENTITY: Ensure the Driver's "Agency" exists
            agency, _ = Agency.objects.get_or_create(
                agency_id=f"DRIVER-{user.username}",
                defaults={
                    'agency_name': f"{user.first_name} {user.last_name}",
                    'agency_url': 'http://cptn.nscc.ca',
                    'agency_timezone': 'America/Halifax'
                }
            )

            # 3. SERVICE: Create the Calendar entry
            service_id = f"SVC-{uuid.uuid4().hex[:8].upper()}"
            Calendar.objects.create(
                service_id=service_id,
                start_date=validated_data['start_date'],
                end_date=validated_data['end_date'],
                monday=1 if 'monday' in days else 0,
                tuesday=1 if 'tuesday' in days else 0,
                wednesday=1 if 'wednesday' in days else 0,
                thursday=1 if 'thursday' in days else 0,
                friday=1 if 'friday' in days else 0,
                saturday=1 if 'saturday' in days else 0,
                sunday=1 if 'sunday' in days else 0,
            )

            # 4. ROUTE: Link or Create the logical Route
            route, _ = Routes.objects.get_or_create(
                route_id=f"RT-{user.username}-COMMUTE",
                defaults={
                    'agency': agency,
                    'route_short_name': "CPTN",
                    'route_long_name': f"Commute to {destination.stop_name}",
                    'route_type': 3 # Bus/Carpool
                }
            )

            # 5. SPATIAL: Call ORS and Save the Shape
            client = openrouteservice.Client(key=settings.ORS_API_KEY)
            coords = (
                (origin.area_lon, origin.area_lat), 
                (destination.stop_lon, destination.stop_lat)
            )
            
            ors_res = client.directions(coordinates=coords, profile='driving-car', format='geojson')
            line_coords = ors_res['features'][0]['geometry']['coordinates']
            duration_seconds = ors_res['features'][0]['properties']['summary']['duration']

            shape = Shapes.objects.create(
                shape_id=f"SHP-{uuid.uuid4().hex[:8]}",
                geometry=LineString(line_coords)
            )

            # 6. TRIP: Create the Trip Master Record
            trip = Trips.objects.create(
                trip_id=f"TRP-{uuid.uuid4().hex[:12]}",
                route=route,
                service_id=service_id,
                shape=shape,
                trip_headsign=destination.stop_name,
                driver=user
            )

            # 7. STOP TIMES: Define the Journey start and end
            # Origin
            StopTimes.objects.create(
                trip=trip,
                stop_id=destination.stop_id, # Simplified: Using dest for sequence 0 metadata
                stop_sequence=0,
                arrival_time=self._to_duration(validated_data['departure_time']),
                departure_time=self._to_duration(validated_data['departure_time'])
            )
            # Destination
            arrival_at_dest = self._to_duration(validated_data['departure_time']) + timedelta(seconds=duration_seconds)
            StopTimes.objects.create(
                trip=trip,
                stop=destination,
                stop_sequence=1,
                arrival_time=arrival_at_dest,
                departure_time=arrival_at_dest
            )

            # 8. FREQUENCY: Optional Shuttle Logic
            if validated_data.get('end_time') and validated_data.get('headway_minutes'):
                Frequencies.objects.create(
                    trip=trip,
                    start_time=self._to_duration(validated_data['departure_time']),
                    end_time=self._to_duration(validated_data['end_time']),
                    headway_secs=validated_data['headway_minutes'] * 60
                )

            # 9. CAPACITY: Initialize the seats
            CPTNTripCapacity.objects.create(
                trip=trip,
                total_seats=validated_data['available_seats'],
                available_seats=validated_data['available_seats']
            )

        return trip

    def _to_duration(self, time_obj):
        """Helper to convert datetime.time to timedelta for DurationField"""
        return timedelta(hours=time_obj.hour, minutes=time_obj.minute, seconds=time_obj.second)
    

# ==========================================
# SECTION 5: BOOKING & REQUESTS
# ==========================================

class RideRequestSerializer(serializers.ModelSerializer):
    rider_name = serializers.ReadOnlyField(source='rider.get_full_name')
    rider_email = serializers.ReadOnlyField(source='rider.email')

    class Meta:
        model = CPTNRideRequest
        fields = ['request_id', 'trip', 'rider', 'rider_name', 'rider_email', 'status']
        read_only_fields = ['request_id', 'status']