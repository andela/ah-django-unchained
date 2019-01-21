from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from authors.apps.authentication.models import User


class BaseTestCase(TestCase):
    """Base tests to be used by all other tests"""
    def setUp(self):
        self.client = APIClient()
        self.register_url = reverse('authentication:auth-register')
        self.login_url = reverse("authentication:auth-login")
        self.new_user = {
            "username": "andrew",
            "email": "andrewhinga5@gmail.com",
            "password": "g@_Gigz-2416"
            }

        self.username = "testuser"
        self.email = "testuser@gmail.com"
        self.password = "this_user123@A"

        self.test_user = User.objects.create_user(
            username=self.username,
            email=self.email,
            password=self.password)

        self.test_user1 = User.objects.create_user(
            username="andrew",
            email="andrewhinga5@gmail.com",
            password="g@_Gigz-2416")

        self.data_for_test = {"user": {
            "email": self.email,
            "password": self.password
        }}

        response = self.client.post(
            self.login_url, self.data_for_test, format='json')

        self.token = response.data["token"]
        self.assertEqual(response.status_code, status.HTTP_200_OK)
