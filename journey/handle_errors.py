from rest_framework.response import Response
from rest_framework import status
import logging
import uuid

logger = logging.getLogger(__name__)

def handle_api_errors(error_type, message=None, exception=None):
    error_id = uuid.uuid4()
    response_data = {
        "errorID": str(error_id),
        "exception": str(exception) if exception else None,
        "type": error_type,
        "message": message or "An unknown error occurred."
    }

    if error_type == 'bad_request':
        response_data["status"] = status.HTTP_400_BAD_REQUEST
    elif error_type == 'unauthorized':
        response_data["status"] = status.HTTP_401_UNAUTHORIZED
    elif error_type == 'forbidden':
        response_data["status"] = status.HTTP_403_FORBIDDEN
    elif error_type == 'not_found':
        response_data["status"] = status.HTTP_404_NOT_FOUND
    elif error_type == 'internal_api_server_error':
        logger.exception(f"Unexpected error: {error_id}", exc_info=exception)
        response_data["status"] = status.HTTP_500_INTERNAL_SERVER_ERROR
    elif error_type == 'too_many_requests':
        response_data["status"] = status.HTTP_429_TOO_MANY_REQUESTS
    else:
        response_data["status"] = status.HTTP_400_BAD_REQUEST

    return Response(response_data, status=response_data["status"])