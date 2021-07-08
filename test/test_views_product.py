from myapi.models import Product
from myapi.serializers import ProductSerializer
from .test_setup import TestSetUp
from django.urls import reverse
from rest_framework import status
import json


class TestProduct(TestSetUp):
    def test_product_isNotAuthenticated(self):
        res = self.client.get(reverse('products'))

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(json.loads(res.content), {
                         'message': 'You must login first'})

    def test_product_get_all(self):
        login = self.client.post(reverse('login'), self.user_login)

        headers = {
            'HTTP_AUTHORIZATION': 'Bearer ' + login.data['access']
        }
        res = self.client.get(reverse('products'), **headers)

        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)
