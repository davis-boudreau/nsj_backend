from django.contrib.gis.db import models
from django.contrib.auth.models import User
import uuid

# ==========================================
# SECTION 1: IDENTITY & FEED METADATA
# ==========================================

class CPTNUserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    agency = models.ForeignKey('Agency', on_delete=models.SET_NULL, null=True, blank=True)
    is_driver = models.BooleanField(default=False)
    is_rider = models.BooleanField(default=True)
    vehicle_desc = models.CharField(max_length=255, blank=True)
    default_seats = models.PositiveIntegerField(default=0)

class Agency(models.Model):
    agency_id = models.CharField(max_length=100, primary_key=True)
    agency_name = models.CharField(max_length=255)
    agency_url = models.URLField()
    agency_timezone = models.CharField(max_length=50, default="America/Halifax")
    agency_lang = models.CharField(max_length=10, blank=True, null=True)
    agency_phone = models.CharField(max_length=20, blank=True, null=True)
    agency_email = models.EmailField(blank=True, null=True)

class FeedInfo(models.Model):
    feed_publisher_name = models.CharField(max_length=255)
    feed_publisher_url = models.URLField()
    feed_lang = models.CharField(max_length=10)
    default_lang = models.CharField(max_length=10, blank=True, null=True)
    feed_start_date = models.DateField(blank=True, null=True)
    feed_end_date = models.DateField(blank=True, null=True)
    feed_version = models.CharField(max_length=100)
    feed_contact_email = models.EmailField(blank=True, null=True)
    feed_contact_url = models.URLField(blank=True, null=True)

# ==========================================
# SECTION 2: SPATIAL CORE
# ==========================================

class Area(models.Model):
    """
    Modified Area model to support NS GeoNames.
    Corresponds to areas.txt in GTFS-Flexible.
    """
    # GTFS: area_id (We can use the cgndb_key here as it's a unique identifier)
    area_id = models.CharField(max_length=100, primary_key=True)
    
    # GTFS: area_name (The geoname, e.g., 'MacIntyre Lake')
    area_name = models.CharField(max_length=255, blank=True, null=True)
    
    # Custom fields for NS GeoNames metadata
    county = models.CharField(max_length=255, blank=True, null=True)
    location_narrative = models.TextField(blank=True, null=True) # From locn_narr
    
    # Redundant but useful for non-GIS queries/exports
    area_lat = models.FloatField(max_length=50, blank=True, null=True)
    area_lon = models.FloatField(max_length=50, blank=True, null=True)

    # Spatial Point for the center of the Area (nad83_lat/lon converted to WGS84)
    location = models.PointField(srid=4326, blank=True, null=True,help_text="Centroid of the GeoName area")

    def __str__(self):
        return f"{self.area_name} ({self.county})"
    
class Stops(models.Model):
    """Corresponds to stops.txt - The primary location model for CPTN"""
    stop_id = models.CharField(max_length=100, primary_key=True)
    stop_code = models.CharField(max_length=50, blank=True, null=True)
    stop_name = models.CharField(max_length=255)
    stop_desc = models.TextField(blank=True, null=True)
    stop_icon = models.CharField(max_length=255, blank=True, null=True) # Custom field for stop pin image URL
    
    # Redundant but useful for non-GIS queries/exports
    stop_lat = models.FloatField(max_length=50, blank=True, null=True)
    stop_lon = models.FloatField(max_length=50, blank=True, null=True)
    
    # Primary field for GeoDjango spatial lookups
    location = models.PointField(srid=4326)
    
    zone_id = models.CharField(max_length=100, blank=True, null=True)
    location_type = models.IntegerField(default=0) # 0=Stop, 1=Station
    
    parent_station = models.ForeignKey(
        'self', 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='child_stops'
    )

    # Standard GTFS fields used for CPTN metadata
    stop_url = models.URLField(
        max_length=500, 
        blank=True, 
        null=True, 
        help_text="URL for stop pin image (e.g., campus photo)"
    )
    wheelchair_boarding = models.IntegerField(
        choices=[(0, 'No Information'), (1, 'Accessible'), (2, 'Not Accessible')],
        default=0
    )

    # Relationship to GTFS-Flexible Areas
    areas = models.ManyToManyField(
        'Area', 
        through='StopArea', 
        related_name='stops'
    )

    class Meta:
        verbose_name_plural = "Stops"

    def __str__(self):
        return self.stop_name

class StopArea(models.Model):
    """Corresponds to stop_areas.txt - Links Stops to one or more Areas"""
    area = models.ForeignKey(
        'Area', 
        on_delete=models.CASCADE, 
        db_column='area_id'
    )
    stop = models.ForeignKey(
        'Stops', 
        on_delete=models.CASCADE, 
        db_column='stop_id'
    )

    class Meta:
        unique_together = ('area', 'stop')
        verbose_name = "Stop Area Mapping"

class Shapes(models.Model):
    # uuid or slug to link multiple points, but for ORS we'll store the LineString
    shape_id = models.CharField(max_length=100, primary_key=True) 
    # Keep geometry as the primary field for GeoDjango/Leaflet
    geometry = models.LineStringField(srid=4326, null=True, blank=True)

    class Meta:
        verbose_name_plural = "Shapes"

# ==========================================
# SECTION 3: CALENDAR & LOGIC
# ==========================================

class Calendar(models.Model):
    service_id = models.CharField(max_length=100, primary_key=True)
    monday = models.IntegerField(default=0)
    tuesday = models.IntegerField(default=0)
    wednesday = models.IntegerField(default=0)
    thursday = models.IntegerField(default=0)
    friday = models.IntegerField(default=0)
    saturday = models.IntegerField(default=0)
    sunday = models.IntegerField(default=0)
    start_date = models.DateField()
    end_date = models.DateField()

class CalendarDates(models.Model):
    service_id = models.CharField(max_length=100)
    date = models.DateField()
    exception_type = models.IntegerField() # 1: Added, 2: Removed

    class Meta:
        unique_together = ('service_id', 'date')

class BookingRules(models.Model):
    booking_rule_id = models.CharField(max_length=100, primary_key=True)
    booking_type = models.IntegerField() 
    prior_notice_duration_min = models.IntegerField(null=True, blank=True)
    prior_notice_duration_max = models.IntegerField(null=True, blank=True)
    prior_notice_last_day = models.IntegerField(null=True, blank=True)
    message = models.TextField(blank=True, null=True)

# ==========================================
# SECTION 4: ROUTES & TRIPS
# ==========================================

class Routes(models.Model):
    route_id = models.CharField(max_length=100, primary_key=True)
    agency = models.ForeignKey(Agency, on_delete=models.CASCADE)
    route_short_name = models.CharField(max_length=50)
    route_long_name = models.CharField(max_length=255, blank=True)
    route_type = models.IntegerField(default=3)
    
    def __str__(self):
        return self.route_short_name

class Trips(models.Model):
    trip_id = models.CharField(max_length=100, primary_key=True)
    route = models.ForeignKey('Routes', on_delete=models.CASCADE, related_name='trips')
    service_id = models.CharField(max_length=100)
    # Changed shape_id to a ForeignKey to link directly to our Shapes model
    shape = models.ForeignKey(Shapes, on_delete=models.SET_NULL, null=True, blank=True)
    trip_headsign = models.CharField(max_length=255, blank=True)
    
    # Custom fields for Car Pool tracking
    driver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='driven_trips', null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    def __str__(self):
        return f"{self.trip_id} - {self.trip_headsign}"

class StopTimes(models.Model):
    trip = models.ForeignKey(Trips, on_delete=models.CASCADE, related_name='stop_times')
    stop = models.ForeignKey(Stops, on_delete=models.CASCADE)
    stop_sequence = models.PositiveIntegerField()
    arrival_time = models.DurationField()
    departure_time = models.DurationField()
    pickup_type = models.IntegerField(default=0)

    class Meta:
        unique_together = ('trip', 'stop_sequence')

class Frequencies(models.Model):
    trip = models.ForeignKey(Trips, on_delete=models.CASCADE)
    start_time = models.DurationField()
    end_time = models.DurationField()
    headway_secs = models.PositiveIntegerField()
    exact_times = models.IntegerField(default=0)

# ==========================================
# SECTION 5: METADATA & SIDECARS
# ==========================================

class Attributions(models.Model):
    attribution_id = models.CharField(max_length=100, primary_key=True)
    agency = models.ForeignKey(Agency, on_delete=models.SET_NULL, null=True, blank=True)
    route = models.ForeignKey(Routes, on_delete=models.SET_NULL, null=True, blank=True)
    trip = models.ForeignKey(Trips, on_delete=models.SET_NULL, null=True, blank=True)
    organization_name = models.CharField(max_length=255)
    is_producer = models.IntegerField(default=0)
    is_operator = models.IntegerField(default=0)
    is_authority = models.IntegerField(default=0)
    attribution_url = models.URLField(blank=True, null=True)

class Translations(models.Model):
    table_name = models.CharField(max_length=50)
    field_name = models.CharField(max_length=50)
    language = models.CharField(max_length=10)
    translation = models.TextField()
    record_id = models.CharField(max_length=100)

class CPTNRideRequest(models.Model):
    request_id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    trip = models.ForeignKey(Trips, on_delete=models.CASCADE)
    rider = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, default='Pending')

class CPTNTripCapacity(models.Model):
    trip = models.OneToOneField(Trips, on_delete=models.CASCADE, primary_key=True)
    total_seats = models.PositiveIntegerField()
    available_seats = models.PositiveIntegerField()
