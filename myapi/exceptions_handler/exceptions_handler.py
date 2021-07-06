from rest_framework import status
from rest_framework.views import exception_handler
from rest_framework.response import Response


def base_exception_handler(exc, context):

    response = exception_handler(exc, context)

    handlers = {
        "ValidationError": _handle_authentication_error,
        "InvalidToken": _handle_authentication_error,
        "AuthenticationFailed": _handle_authentication_error,
        "NotAuthenticated": _handle_authentication_error
    }

    exception_class = exc.__class__.__name__
    if response is not None:
        if exception_class in handlers:
            return handlers[exception_class](exc, context, response)
    return response


def _handle_authentication_error(exc, context, response):
    handlers = {
        "RegisterView": _handle_register_error
    }
    view_name = context['view'].__class__.__name__
    return handlers[view_name](exc, context, response)


def _handle_register_error(exc, context, response):

    exc_codes = exc.get_codes()
    list_error_fields = response.data.keys()
    list_error_codes = list(exc_codes.values())

    if 'email' in response.data and list_error_codes[0][0] == "blank":
        res = {
            "message": "Fields username, email and password need to be filled",
        }
        return Response(res, status=status.HTTP_400_BAD_REQUEST)
    elif 'email' in response.data and list_error_codes[0][0] == "unique":
        res = {
            "message": "Email has been already used",
        }
        return Response(res, status=status.HTTP_400_BAD_REQUEST)
    elif 'email' in response.data and list_error_codes[0][0] == "invalid":
        res = {
            "message": "Email has to be an email",
        }
        return Response(res, status=status.HTTP_400_BAD_REQUEST)
    elif 'username' in response.data and list_error_codes[0][0] == "unique":
        res = {
            "message": "Username has been already used"
        }
        return Response(res, status=status.HTTP_400_BAD_REQUEST)
    elif 'username' in response.data and list_error_codes[0][0] == "min_length":
        res = {
            "message": "Username is too short"
        }
        return Response(res, status=status.HTTP_400_BAD_REQUEST)
    elif 'password' in response.data and list_error_codes[0][0] == 'min_length':
        res = {
            "message": "Password is too short"
        }
        return Response(res, status=status.HTTP_400_BAD_REQUEST)
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
