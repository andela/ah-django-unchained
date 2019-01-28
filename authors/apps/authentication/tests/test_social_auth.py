import json
import os
from django.urls import reverse
from rest_framework.views import status
from rest_framework.test import APITestCase, APIClient


class SocialAuthTest(APITestCase):
    """Test social authentication funcionality."""
    client = APIClient

    def setUp(self):
        self.social_oauth_url = reverse('authentication:social_auth')
        self.facebook_access_token = os.getenv('FACEBOOK_TOKEN')
        self.oauth1_access_token = os.getenv('TWITTER_TOKEN')
        self.oauth1_access_token_secret = os.getenv('TWITTER_SECRET_TOKEN')
        self.invalid_facebook_access_token = "bhjdvsfi73gyfbudhjvcbdskncoue"
      
        self.invalid_provider = {
            "provider": "faceboook",
            "access_token": self.facebook_access_token
        }
        self.facebook_provider = {
            "provider": "facebook",
            "access_token": self.facebook_access_token
        }
        self.twitter_provider = {
            "provider": "twitter",
            "access_token": self.oauth1_access_token, 
            "access_token_secret": self.oauth1_access_token_secret
        }
        self.invalid_access_token_name = {
            "provider": "facebook",
            "access_token": self.invalid_facebook_access_token
        }
        self.twitter_missing_access_token_secret = {
            "provider": "twitter",
            "access_token": self.oauth1_access_token, 
        }

    def test_rejects_invalid_provider_name(self):
        """Test invalid provider name."""
        response = self.client.post(
            self.social_oauth_url, self.invalid_provider, format='json')
        self.assertEqual(response.data['error'],
                         'Please enter a valid social provider')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_login_with_facebook(self):
        """Test login with facebook."""
        response = self.client.post(
            self.social_oauth_url, self.facebook_provider, format='json')
        self.assertIn('email', response.data)
        self.assertIn('token', response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_login_with_twitter(self):
        """Test login with twitter."""
        response = self.client.post(
            self.social_oauth_url, self.twitter_provider, format='json')
        self.assertIn('email', response.data)
        self.assertIn('token', response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_rejects_login_missing_access_token(self):
        """Test missing token."""
        response = self.client.post(self.social_oauth_url,
                                    data={"provider": 'facebook'},
                                    format='json')
        self.assertEqual(json.loads(response.content),
                         {"errors": {"access_token":
                          ["This field is required."]}})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_rejects_login_missing_provider_name(self):
        """Test missing provider."""
        response = self.client.post(
            self.social_oauth_url,
            data={"access_token": self.facebook_access_token}, format='json')
        self.assertEqual(json.loads(response.content), {"errors": {"provider":
                         ["This field is required."]}})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_rejects_login_missing_access_token(self):
        """Test missing access_token."""
        response = self.client.post(
            self.social_oauth_url,
            data={"provider": "facebook"}, format='json')
        self.assertEqual(json.loads(response.content),
                         {"errors": {"access_token":
                          ["This field is required."]}})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_rejects_invalid_access_token_name(self):
        """Test invalid access token name."""
        response = self.client.post(
            self.social_oauth_url,
            self.invalid_access_token_name, format='json')
        self.assertEqual(response.data['errors'],
                         'Invalid token')
        self.assertEqual(response.status_code,
                         status.HTTP_500_INTERNAL_SERVER_ERROR)

    def test_rejects_missing_access_token_secret_in_twitter(self):
        """Test rejects missing access token secret in twitter."""
        response = self.client.post(
            self.social_oauth_url,
            self.twitter_missing_access_token_secret, format='json')
        self.assertEqual(response.data['error'],
                         'Please enter your secret token')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST) 