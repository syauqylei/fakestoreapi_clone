from rest_framework import status
from rest_framework.response import Response


def _handle_register_error(exc, context, response):

    exc_codes = exc.get_codes()
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


def _handle_login_error(exc, context, response):
    exc_codes = exc.get_codes()

    if 'password' in response.data and exc_codes['password'][0] == 'blank':
        list_error_codes = list(exc_codes.values())
        res = {
            "message": 'Invalid username or password'
        }
        return Response(res, status=status.HTTP_400_BAD_REQUEST)
    elif 'username' in response.data and exc_codes['username'][0] == 'blank':
        res = {
            "message": 'Invalid username or password'
        }
        return Response(res, status=status.HTTP_400_BAD_REQUEST)
    elif 'detail' in response.data and exc_codes == "no_active_account":
        res = {
            "message": 'Invalid username or password'
        }
        return Response(res, status=status.HTTP_400_BAD_REQUEST)
    elif 'detail' in response.data and exc_codes['detail'] == "token_not_valid":
        res = {
            "message": 'Invalid Token'
        }
        return Response(res, status=status.HTTP_401_UNAUTHORIZED)
    return response
