from myapi.models import Product
from myapi.serializers import ProductSerializer
from .test_setup import TestSetUp
from django.urls import reverse
from rest_framework import status
import json


class TestProduct(TestSetUp):
    def setUp(self):
        super().setUp()
        self.login = self.client.post(reverse('login'), self.user_login)

        self.headers = {
            'HTTP_AUTHORIZATION': 'Bearer ' + self.login.data['access']
        }

        self.admin = self.client.post(
            reverse('login'), {'username': 'admin', 'password': 'admin12345'})

        self.headers_admin = {
            'HTTP_AUTHORIZATION': 'Bearer ' + self.admin.data['access']
        }
        self.product = {
            'title': 'crewneck gray',
            'price': 12,
            'category': "men's clothing",
            'description': 'sweater for man',
            'image': 'https://picsum.photos/200/300'
        }

    def test_product_isNotAuthenticated(self):
        res = self.client.get(reverse('products'))

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(json.loads(res.content), {
                         'message': 'You must login first'})

    def test_product_get_all(self):
        res = self.client.get(reverse('products'), **self.headers)

        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_product_get_single(self):
        product = Product.objects.all()[0]

        getOne = self.client.get(
            reverse('products_detail', kwargs={'pk': product.pk}), **self.headers)

        serializer = ProductSerializer(product)

        self.assertEqual(getOne.status_code, status.HTTP_200_OK)
        self.assertEqual(getOne.data, serializer.data)

    def test_product_get_single_notFound(self):
        product_id = 12321312238122039

        getOne = self.client.get(
            reverse('products_detail', kwargs={'pk': product_id}), **self.headers)

        self.assertEqual(getOne.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(getOne.data, {'message':  "The product is not found"})

    def test_product_create_success(self):
        createOne = self.client.post(
            reverse('products'), self.product, **self.headers_admin)

        serializer = ProductSerializer(self.product)
        print(serializer.data)
        self.assertEqual(createOne.status_code, status.HTTP_201_CREATED)
        self.assertEqual(createOne.data, {
                         "message": f"Product {self.product[ 'title' ]} has been created"})

    def test_product_create_notStaff(self):
        createOne = self.client.post(
            reverse('products'), self.product, **self.headers)

        self.assertEqual(createOne.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(createOne.data, {
                         "message": f"You're not a staff"})

    def test_product_validators_error_empty_str(self):
        product = self.product
        product['title'] = ''
        createOne = self.client.post(
            reverse('products'), product, **self.headers_admin)

        self.assertEqual(createOne.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertTrue('error' in createOne.data)
        self.assertTrue(isinstance(createOne.data['error'], list))
        self.assertEqual(createOne.data['error'], [
                         {"name": 'ValidationError', 'message': 'You entered an empty string to title field'}])

    def test_product_validators_error_no_title(self):
        product = self.product
        del product['title']
        createOne = self.client.post(
            reverse('products'), product, **self.headers_admin)
        self.assertEqual(createOne.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertTrue('error' in createOne.data)
        self.assertTrue(isinstance(createOne.data['error'], list))
        self.assertEqual(createOne.data['error'], [
                         {"name": 'ValidationError', 'message': 'Title is required'}])

    def test_product_validators_error_no_price(self):
        product = self.product
        del product['price']

        createOne = self.client.post(
            reverse('products'), product, **self.headers_admin)

        self.assertEqual(createOne.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertTrue('error' in createOne.data)
        self.assertTrue(isinstance(createOne.data['error'], list))
        self.assertEqual(createOne.data['error'], [
            {'name': 'ValidationError', 'message': 'Price is required'}
        ])

    def test_product_validators_error_no_category(self):
        product = self.product
        del product['category']

        createOne = self.client.post(
            reverse('products'), product, **self.headers_admin
        )

        self.assertEqual(createOne.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertTrue('error' in createOne.data)
        self.assertTrue(isinstance(createOne.data['error'], list))
        self.assertEqual(createOne.data['error'], [
            {'name': 'ValidationError', 'message': 'Category is required'}
        ])

    def test_product_validators_error_no_category_blank(self):
        product = self.product
        product['category'] = ''

        createOne = self.client.post(
            reverse('products'), product, **self.headers_admin
        )

        self.assertEqual(createOne.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertTrue('error' in createOne.data)
        self.assertTrue(isinstance(createOne.data['error'], list))
        self.assertEqual(createOne.data['error'], [
            {'name': 'ValidationError', 'message': 'Category is required'}
        ])
