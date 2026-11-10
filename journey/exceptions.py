from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status

def custom_exception_handler(exc, context):
    """
    Custom exception handler that modifies error responses.
    """
    # Call the default exception handler first
    response = exception_handler(exc, context)

    if response is not None:
        # Customize the default error response
        response.data['status_code'] = response.status_code
    else:
        # Handle any unhandled exceptions
        response = Response(
            {"error": "An unexpected error occurred."},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

    return response