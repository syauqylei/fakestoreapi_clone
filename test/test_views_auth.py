import pytest
import json
from .test_setup import TestSetUp
from django.urls import reverse


class TestRegister(TestSetUp):
    def test_user_cannot_register_with_empty_data(self):
        res = self.client.post(
            reverse('register'), {'username': '', 'email': '', 'password': ''})

        self.assertEqual(res.status_code, 400)
        self.assertEqual(json.loads(res.content), {
                         'message': 'Fields username, email and password need to be filled'})

    def test_user_cannot_register_with_existed_username(self):
        res = self.client.post(reverse('register'),
                               self.user_data_existed_username)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(json.loads(res.content), {
                         'message': 'Username has been already used'})

    def test_user_cannot_register_with_username_too_short(self):
        res = self.client.post(reverse('register'),
                               self.user_data_username_too_short)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(json.loads(res.content), {
                         'message': 'Username is too short'})

    def test_user_cannot_register_with_password_too_short(self):
        res = self.client.post(reverse('register'),
                               self.user_data_password_too_short)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(json.loads(res.content), {
                         'message': 'Password is too short'})

    def test_user_cannot_register_with_existed_email(self):
        res = self.client.post(reverse('register'),
                               self.user_data_existed_email)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(json.loads(res.content), {
                         'message': 'Email has been already used'})

    def test_user_cannot_register_with_email_thats_not_email(self):
        res = self.client.post(reverse('register'),
                               self.user_data_email_isNot_email)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(json.loads(res.content), {
                         'message': 'Email has to be an email'})

    def test_user_can_register(self):
        res = self.client.post(reverse('register'), self.user_data_correct)

        self.assertEqual(res.status_code, 201)
        self.assertEqual(json.loads(res.content), {
                         'message': f"User {self.user_data_correct['username']} has been created"})


class TestLogin(TestSetUp):
    def test_user_can_login(self):
        res = self.client.post(reverse('login'), self.user_login)

        self.assertHasAttr(json.loads(res.content), 'access')
        self.assertHasAttr(json.loads(res.content), 'refresh')
        self.assertEqual(res.status_code, 200)

    def test_user_cannot_login_wrong_password(self):
        user = self.user_login
        user['password'] = 'password1233'
        res = self.client.post(reverse('login'), user)

        self.assertEqual(json.loads(res.content), {
                         'message': 'Invalid username or password'})
        self.assertEqual(res.status_code, 400)

    def test_user_cannot_login_empty_password(self):
        user = self.user_login
        user['password'] = ''
        res = self.client.post(reverse('login'), user)

        self.assertEqual(json.loads(res.content), {
                         'message': 'Invalid username or password'})
        self.assertEqual(res.status_code, 400)

    def test_user_cannot_login_wrong_username(self):
        user = self.user_login
        user['username'] = 'rindu12345'
        res = self.client.post(reverse('login'), user)

        self.assertEqual(json.loads(res.content), {
                         'message': 'Invalid username or password'})
        self.assertEqual(res.status_code, 400)

    def test_user_cannot_login_empty_username(self):
        user = self.user_login
        user['username'] = ''
        res = self.client.post(reverse('login'), user)

        self.assertEqual(json.loads(res.content), {
                         'message': 'Invalid username or password'})
        self.assertEqual(res.status_code, 400)


class TestLoginRefresh(TestSetUp):
    def setUp(self):
        super().setUp()
        self.res = self.client.post(reverse('login'), self.user_login)
        self.refreshToken = self.res.data['refresh']

        self.assertEqual(self.res.status_code, 200)
        self.assertTrue('access' in self.res.data)
        self.assertTrue('refresh' in self.res.data)

    def test_user_can_refresh_token(self):
        resRefresh = self.client.post(
            reverse('refresh_token'), {'refresh': self.refreshToken})

        self.assertEqual(resRefresh.status_code, 200)
        self.assertTrue('access' in resRefresh.data)

    def test_user_cannot_refresh_token_with_wrong_token(self):
        resRefresh = self.client.post(
            reverse('refresh_token'), {'refresh': 'asdasm,sad'})

        self.assertEqual(resRefresh.status_code, 401)
        self.assertEqual(json.loads(resRefresh.content),
                         {'message': 'Invalid Token'})
