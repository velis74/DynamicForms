from rest_framework import status
from rest_framework.exceptions import APIException


class DynamicFormsApiException(APIException):
    pass


class ServiceNotImplementedApiException(DynamicFormsApiException):
    status_code = status.HTTP_501_NOT_IMPLEMENTED
    default_detail = 'Service not implemented.'
    default_code = 'service_not_implemented'
