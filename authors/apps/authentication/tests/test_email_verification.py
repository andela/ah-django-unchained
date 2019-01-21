import os
from django.urls import reverse
from django.core import mail
from django.conf import settings
from rest_framework.test import APIClient
from rest_framework.test import APITestCase
from rest_framework.views import status
from ..utils import send_link


class TestEmailVerification(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.signup_url = reverse('authentication:auth-register')
        self.login_url = reverse('authentication:auth-login')
        self.resend_verify_url = reverse('authentication:auth-reverify')

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
        self.register_response = self.client.post(self.signup_url,
                                                  self.signup_data,
                                                  format='json')

    def test_send_email(self):
        # Empty the test outbox
        mail.outbox = []
        self.assertEqual(len(mail.outbox), 0)
        mail.send_mail(
            'Authors Haven Verification Link', 'Here is the message.',
            settings.EMAIL_HOST_USER, ['daveyhash@gmail.com'],
            fail_silently=False,
        )
        # Test that one message has been sent.
        self.assertEqual(len(mail.outbox), 1)
        # Verify that the subject of the first message is correct.
        self.assertEqual(mail.outbox[0].subject,
                         'Authors Haven Verification Link')

    def test_verify_account(self):
        token = self.register_response.data['token']
        verify_url = reverse('authentication:auth-verify',
                             kwargs={"token": token})
        response = self.client.get(
            verify_url, HTTP_AUTHORIZATION='token {}'.format(token))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_already_verified_account(self):
        token = self.register_response.data['token']
        verify_url = reverse('authentication:auth-verify',
                             kwargs={"token": token})
        response1 = self.client.get(
            verify_url, HTTP_AUTHORIZATION='token {}'.format(token))
        self.assertEqual(response1.status_code, status.HTTP_200_OK)
        response2 = self.client.get(
            verify_url, HTTP_AUTHORIZATION='token {}'.format(token))
        self.assertEqual(response2.status_code, status.HTTP_403_FORBIDDEN)

    def test_verify_account_bad_token(self):
        token = self.register_response.data['token']
        verify_url = reverse('authentication:auth-verify',
                             kwargs={"token": 404040})
        response = self.client.get(
            verify_url, HTTP_AUTHORIZATION='token {}'.format(token))
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, {"errors": {
            "email": [
                "Verification link is invalid."
            ]}
        })

    def test_resend_verification_link(self):
        token = self.register_response.data['token']
        response = self.client.get(
            self.resend_verify_url, HTTP_AUTHORIZATION='token {}'.format(token))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {
            "message": "Verification link sent successfully. Please check your email.",
        })
