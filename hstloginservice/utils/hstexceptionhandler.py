
from rest_framework.views import exception_handler
from django.http import JsonResponse
from rest_framework import serializers

def hst_exception_handler(exc, context):
    # Call REST framework's default exception handler first,
    # to get the standard error response.
    response = exception_handler(exc, context)
    
    if isinstance(exc, serializers.ValidationError):
        return JsonResponse({'error': response.data[0]}, status=response.status_code)

    return JsonResponse({'error': response.data['detail']}, status=response.status_code)