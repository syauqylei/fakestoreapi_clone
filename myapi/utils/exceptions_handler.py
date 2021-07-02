from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework_simplejwt.views import (TokenObtainPairView,)


def base_exception_handler(exc, context):
    response = exception_handler(exc, context)

    if response is not None:
        exc_codes = exc.get_codes()
        if context['view'].get_view_name() == "Register":
            list_error_fields = response.data.keys()
            list_error_codes = list(exc_codes.values())

            if len(list_error_fields) == 1:
                if 'email' in response.data:
                    if exc_codes['email'][0] == 'unique':
                        message = response.data['email'][0]
                        return Response({'message': message}, status=status.HTTP_400_BAD_REQUEST)
                    elif exc_codes['email'][0] == 'invalid':
                        message = 'Email has to be an email'
                        return Response({'message': message}, status=status.HTTP_400_BAD_REQUEST)
                elif 'username' in response.data:
                    if exc_codes['username'][0] == 'unique':
                        message = response.data['username'][0]
                        return Response({'message': message}, status=status.HTTP_400_BAD_REQUEST)
                    elif exc_codes['username'][0] == 'min_length':
                        message = 'Username is too short'
                        return Response({'message': message}, status=status.HTTP_400_BAD_REQUEST)
                elif 'password' in response.data:
                    if exc_codes['password'][0] == 'min_length':
                        message = 'Password is too short'
                        return Response({'message': message}, status=status.HTTP_400_BAD_REQUEST)
            else:
                if list_error_codes[0][0] == 'blank':
                    message = 'Fields username, email and password need to be filled'
                    return Response({'message': message}, status=status.HTTP_400_BAD_REQUEST)
        elif context['view'].get_view_name() == 'Token Obtain Pair':
            if exc_codes == "no_active_account":
                return Response({'message': 'Invalid username or password'}, status=status.HTTP_400_BAD_REQUEST)
            elif 'username' or 'password' in exc_codes:
                return Response({'message': 'Invalid username or password'}, status=status.HTTP_400_BAD_REQUEST)

    return response
