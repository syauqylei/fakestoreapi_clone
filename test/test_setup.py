from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from django.urls import reverse


class TestSetUp(APITestCase):
    def setUp(self):
        self.user_data_correct = {
            'email': 'syauqilenterano@gmail.com',
            'username': 'syauqylei',
            'password': 'password123'
        }

        self.user_data_existed_email = {
            'email': 'rindu@mail.com',
            'username': 'syauqylei123',
            'password': 'password123'
        }
        self.user_data_email_isNot_email = {
            'email': 'syauqilenterano',
            'username': 'syauqylei123',
            'password': 'password123'
        }
        self.user_data_existed_username = {
            'email': 'syauqylenterano@gmail.com',
            'username': 'rindu123',
            'password': 'password123'
        }
        self.user_data_username_too_short = {
            'email': 'syauqylenterano123@gmail.com',
            'username': 'la',
            'password': 'password123'
        }
        self.user_data_password_too_short = {
            'email': 'syauqylenterano1234@gmail.com',
            'username': 'rindu1ss',
            'password': '123'
        }
        self.user_login = {
            'username': 'rindu123',
            'password': 'password123'
        }
        self.user = User.objects.create_user(
            username="rindu123", password="password123", email="rindu@mail.com")
        self.user_admin = User.objects.create_user(
            username="admin", password="admin12345", email="admin@mail.com")
        self.user_admin.is_staff = True
        self.user_admin.save()

        return super().setUp()

    def tearDown(self):
        return super().tearDown()

    def assertHasAttr(self, obj, intendedAttr):
        testBool = intendedAttr in obj

        self.assertTrue(
            testBool, msg=f'obj lacking an attribute. {obj=}, {intendedAttr=}')
