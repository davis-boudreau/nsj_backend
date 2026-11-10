import csv
from django.core.management.base import BaseCommand
from django.contrib.gis.geos import Point
from django.contrib.gis.db.models.functions import Distance
from django.contrib.gis.measure import D
from journey.models import Area, Stops, StopArea

class Command(BaseCommand):
    help = 'Imports Stops and Areas from CSV and links them spatially'

    def add_arguments(self, parser):
        parser.add_argument('--stops', type=str, help='Path to stops csv')
        parser.add_argument('--areas', type=str, help='Path to geonames csv')
        parser.add_argument('--dist', type=int, default=15, help='Distance in km to link stops to areas')

    def handle(self, *args, **options):
        # 1. Import Areas (GeoNames)
        if options['areas']:
            self.stdout.write("Importing Areas...")
            with open(options['areas'], 'r', encoding='utf-8-sig') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    lon = float(row['nad83_lon'])
                    lat = float(row['nad83_lat'])
                    Area.objects.update_or_create(
                        area_id=row['cgndb_key'],
                        defaults={
                            'area_name': row['geoname'],
                            'county': row['county'],
                            'location_narrative': row['locn_narr'],
                            'area_lat': lat,
                            'area_lon': lon,
                            'location': Point(lon, lat, srid=4326)
                        }
                    )

        # 2. Import Stops (NSCC Campuses)
        if options['stops']:
            self.stdout.write("Importing Stops...")
            with open(options['stops'], 'r', encoding='utf-8-sig') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    lon = float(row['stop_lon'])
                    lat = float(row['stop_lat'])
                    Stops.objects.update_or_create(
                        stop_id=row['stop_id'],
                        defaults={
                            'stop_name': row['stop_name'],
                            'stop_desc': row['stop_desc'],
                            'stop_lat': lat,
                            'stop_lon': lon,
                            'stop_url': row['stop_url'],
                            'stop_icon': row['stop_icon'],
                            'location': Point(lon, lat, srid=4326)
                        }
                    )

        # 3. Spatial Linking (The "Logic" Step)
        self.stdout.write(f"Linking Stops to Areas within {options['dist']}km...")
        self.link_stops_to_areas(options['dist'])

    def link_stops_to_areas(self, distance_km):
        """
        For every Area, find Stops within X km and create a StopArea record.
        Using GeoDjango's native spatial distance lookups.
        """
        all_areas = Area.objects.all()
        for area in all_areas:
            # Find stops within the specified distance of this area centroid
            nearby_stops = Stops.objects.filter(
                location__distance_lte=(area.location, D(km=distance_km))
            )

            for stop in nearby_stops:
                StopArea.objects.get_or_create(area=area, stop=stop)
                
        self.stdout.write(self.style.SUCCESS('Successfully linked network!'))