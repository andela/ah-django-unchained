import json
from django.urls import reverse
from rest_framework.views import status
from rest_framework.test import APITestCase, APIClient


class LoginTestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.login_url = reverse('authentication:auth-login')
        self.signup_url = reverse('authentication:auth-register')
        self.signup_data = {
            "user": {
                "username": "MaryGigz",
                "email": "jake@jake.jake",
                "password": "g@_Gigz-2416"
                }}
        self.login_data = {
            "user": {
                "email": "jake@jake.jake",
                "password": "g@_Gigz-2416"
                }}
        self.login_unregistered_user_data = {
            "user": {
                "email": "jake@jake.jake",
                "password": "jakejake"
                }}

    def test_login(self):
        """if user is registered"""
        register = self.client.post(self.signup_url,
                                    self.signup_data,
                                    format='json')
        self.assertEqual(register.status_code, status.HTTP_201_CREATED)
        """Test if user can login"""
        response = self.client.post(self.login_url,
                                    self.login_data,
                                    format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('email', response.data)
        self.assertIn('username', response.data)
        self.assertIn('token', response.data)

    def test_login_unregistered_user(self):
        """Test login for unregistered users"""
        response = self.client.post(self.login_url,
                                    self.login_unregistered_user_data,
                                    format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(json.loads(response.content), {'errors':
                                                        {'error':
                                                         ['A user with this'
                                                          ' email and password'
                                                          ' was not found.']}})
