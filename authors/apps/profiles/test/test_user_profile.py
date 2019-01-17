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
                "username": "johndoe",
                "email": "john@gmail.com",
                "password": "@Qwerty12345"
                }}
        self.profile_data = {
            "first_name":"","last_name":"",
            "gender":"M","bio":"","profile_image":None}

    def test_get_profile(self):
        """Test get profile upon registrations"""
        register = self.client.post(self.signup_url,self.signup_data,format='json')
        self.assertEqual(register.status_code, status.HTTP_201_CREATED)
        profile = self.client.get('/users/profile/johndoe/',format='json')
        self.assertEqual(self.profile_data,profile.data)
