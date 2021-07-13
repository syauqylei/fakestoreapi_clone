from rest_framework import status
from rest_framework.views import exception_handler
from rest_framework.response import Response
from .error_auth import _handle_register_error, _handle_login_error
from .error_product import _handle_product_error


def base_exception_handler(exc, context):
    response = exception_handler(exc, context)
    handlers = {
        "RegisterView": _handle_register_error,
        "TokenObtainPairView": _handle_login_error,
        "TokenRefreshView": _handle_login_error,
        "ProductList": _handle_product_error,
        "ProductDetail": _handle_product_error
    }
    view_name = context['view'].__class__.__name__
    if response is not None:
        if view_name in handlers:
            return handlers[view_name](exc, context, response)
    return response


def _handle_generic_error(exc, context, response):
    view_name = context['view'].__class__.__name__
    if exc.status_code == 400:
        if "RegisterView" == view_name:
            if exc.get_codes():
                response = {
                    "message": "Fields username, email and password need to be filled",
                }
            return Response(response, status=status.HTTP_400_BAD_REQUEST)
    return response
