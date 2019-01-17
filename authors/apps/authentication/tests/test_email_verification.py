import json
import jwt
import os
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework.test import APITestCase
from rest_framework.views import status
from authors.settings import SECRET_KEY


class TestEmailVerification(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.signup_url = reverse('authentication:auth-register')
        self.login_url = reverse('authentication:auth-login')

        self.signup_data = {
            "user": {
                "username": "kahara12345",
                "email": "daveyhash@gmail.com",
                "password": "H^&lh123d"
            }}
        self.login_data = {
            "user": {
                "email": "daveyhash@gmail.com",
                "password": "H^&lh123d"
            }}

    def test_email_verification(self):
        """test user email verification"""
        response = self.client.post(self.signup_url, self.signup_data,
                                    format="json")
        self.token = response.data['token']
        """Test if unverified user can login"""
        response = self.client.post(self.login_url,
                                    self.login_data,
                                    format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(json.loads(response.content), {'errors': {'error': [
                         'Please verify your account by clicking on the link sent to your email.']}})
