import json
from django.urls import reverse
from django.core import mail
from rest_framework.views import status
from rest_framework.test import APITestCase, APIClient


class ResetPasswordTestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.password_reset_url = reverse('authentication:passwordreset')
        self.password_update_url = "authentication:passwordresetdone"
        self.signup_url = reverse('authentication:auth-register')
        self.signup_data = {
            "user": {
                "username": "MaryGigz",
                "email": "chegemaggie1@gmail.com",
                "password": "g@_Gigz-2416"
                }}
        self.email = {
            "email": "chegemaggie1@gmail.com"
        }
        self.email_not_registered = {
            "email": "kenna@gmail.com"
        }
        self.test_update_password_data = {
            "password": "Jake@1234",
            "confirm_password": "Jake@1234"

        }

    def test_email_not_registered(self):
        """Test if user that is not registered can get the email"""
        response = self.client.post(self.password_reset_url,
                                    self.email_not_registered,
                                     format ="json")
        self.assertEqual(response. status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(json.loads(response.content), {'errors': {'email':
                                                        ['User with this email doesnot exist.']}})

    def test_send_email(self):
        """First register a new user and check if user is registered"""
        register = self.client.post(self.signup_url,
                                    self.signup_data,
                                    format='json')
        self.assertEqual(register.status_code, status.HTTP_201_CREATED)
        response = self.client.post(self.password_reset_url,
                                    self.email,
                                    format ="json")
        self.assertEqual(response. status_code, status.HTTP_200_OK)
        self.assertEqual(json.loads(response.content), {'Message':
                                                        'Successfully sent.Check your email'})
