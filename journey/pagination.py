from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response

class StandardResultsPagination(LimitOffsetPagination):
    default_limit = 10
    max_limit = 50

    def get_paginated_response(self, data):
        # We keep the structure consistent so your JS doesn't break
        return Response({
            'count': self.count,
            'next': self.get_next_link(),
            'previous': self.get_previous_link(),
            'results': data # This will be your FeatureCollection
        })