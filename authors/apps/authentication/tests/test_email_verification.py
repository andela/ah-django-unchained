import json
import jwt
import os
from django.urls import reverse
from django.core import mail
from rest_framework.test import APIClient
from rest_framework.test import APITestCase
from rest_framework.views import status
from authors.settings import SECRET_KEY,EMAIL_HOST_USER


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


    def test_send_verification_email(self):
        # Send message.
        self.assertEqual(len(mail.outbox),0)
        mail.send_mail(
            'Authors Haven Verification Link', 'Here is the message.',
            EMAIL_HOST_USER, ['daveyhash@gmail.com'],
            fail_silently=False,
        )

        # Test that one message has been sent.
        self.assertEqual(len(mail.outbox), 1)

        # Verify that the subject of the first message is correct.
        self.assertEqual(mail.outbox[0].subject, 'Authors Haven Verification Link')



