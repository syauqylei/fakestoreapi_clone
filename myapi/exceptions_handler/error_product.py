from rest_framework import status
from rest_framework.response import Response


def _handle_product_list(exc, context, response):
    if 'not_authenticated' == exc.get_codes():
        res = {
            'message': 'You must login first'
        }
        return Response(res, status=status.HTTP_401_UNAUTHORIZED)
    return response
