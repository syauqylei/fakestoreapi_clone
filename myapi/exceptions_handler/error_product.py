from rest_framework import status
from rest_framework.response import Response


def _handle_product_error(exc, context, response):
    exc_name = exc.__class__.__name__
    if exc_name is not 'ValidationError':
        if 'not_authenticated' == exc.get_codes():
            res = {
                'message': 'You must login first'
            }
            return Response(res, status=status.HTTP_401_UNAUTHORIZED)
        elif 'product_not_found' == exc.get_codes():
            res = {
                'message': str(exc.detail)
            }
            return Response(res, status=status.HTTP_404_NOT_FOUND)
        elif 'permission_denied' == exc.get_codes():
            res = {
                'message': str(exc.detail)
            }
            return Response(res, status=status.HTTP_403_FORBIDDEN)
    else:
        exc_codes = exc.get_codes()
        res = {
            'error': []
        }
        if 'title' in exc_codes and exc_codes['title'][0] == 'blank':
            res['error'].append(
                {'name': 'ValidationError', 'message': 'You entered an empty string to title field'})
            return Response(res, status=status.HTTP_400_BAD_REQUEST)
        elif 'title' in exc_codes and exc_codes['title'][0] == 'required':
            res['error'].append(
                {'name': 'ValidationError', 'message': 'Title is required'})
            return Response(res, status=status.HTTP_400_BAD_REQUEST)
        elif 'price' in exc_codes and exc_codes['price'][0] == 'required':
            res['error'].append(
                {'name': 'ValidationError', 'message': 'Price is required'}
            )
            return Response(res, status=status.HTTP_400_BAD_REQUEST)
    return response
