import django_filters
from .models import Origin, Stops

class OriginFilter(django_filters.FilterSet):
    # Lookup expressions (icontains, iexact)
    geoname = django_filters.CharFilter(lookup_expr='icontains')
    county = django_filters.CharFilter(lookup_expr='icontains')
    nad83_lat__gt = django_filters.NumberFilter(field_name='nad83_lat', lookup_expr='gt')
    nad83_lon__lt = django_filters.NumberFilter(field_name='nad83_lon', lookup_expr='lt')
    objectid__in = django_filters.CharFilter(method='filter_objectid_in')

    def filter_objectid_in(self, queryset, name, value):
        # The name parameter is required by the method signature but is not used in the custom filtering logic. 
        # It is included to conform to the expected parameters for custom filter methods in django_filters
        # Value will be a comma-separated string (e.g., "1,2,3")
        try:
            ids = [int(id.strip()) for id in value.split(',')]
            return queryset.filter(objectid__in=ids)
        except ValueError:
            # Handle cases where the input is not numeric.
            return queryset.none()  # Return an empty queryset or raise an error.

    class Meta:
        model = Origin
        fields = ['objectid', 'geoname', 'county', 'nad83_lat', 'nad83_lon']

class StopsFilter(django_filters.FilterSet):
    # Lookup expressions (icontains, iexact)
    stop_name = django_filters.CharFilter(lookup_expr='icontains')
    stop_desc = django_filters.CharFilter(lookup_expr='icontains')
    stop_lat__gt = django_filters.NumberFilter(field_name='stop_lat', lookup_expr='gt')
    stop_lon__lt = django_filters.NumberFilter(field_name='stop_lon', lookup_expr='lt')
    stop_id__in = django_filters.CharFilter(method='filter_stop_id_in')

    def filter_stop_id_in(self, queryset, name, value):
        # Value will be a comma-separated string (e.g., "NSCC_AL,NSCC_AH,NSCC_AN")
        try:
            ids = [id.strip() for id in value.split(',')]
            return queryset.filter(stop_id__in=ids)
        except ValueError:
            # Handle cases where the input is not valid.
            return queryset.none()  # Return an empty queryset or raise an error.

    class Meta:
        model = Stops
        fields = ['stop_id', 'stop_name', 'stop_desc', 'stop_lat', 'stop_lon']