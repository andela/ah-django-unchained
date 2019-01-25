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
        self.google_access_token = os.getenv('GOOGLE_TOKEN')
        self.facebook_access_token = os.getenv('FACEBOOK_TOKEN')
        self.oauth1_access_token = os.getenv('TWITTER_TOKEN')
        self.oauth1_access_token_secret = os.getenv('TWITTER_SECRET_TOKEN')
      
        self.invalid_provider = {
            "provider": "google-oauth21",
            "access_token": self.google_access_token

        }
        self.google_provider = {
            "provider": "google-oauth2",
            "access_token": self.google_access_token
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

    def test_rejects_invalid_provider_name(self):
        """Test invalid provider name."""
        response = self.client.post(
            self.social_oauth_url, self.invalid_provider, format='json')
        self.assertEqual(response.data['error'],
                         'Please enter a valid social provider')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_login_with_google(self):
        """Test login with google"""
        response = self.client.post(
            self.social_oauth_url, self.google_provider, format='json')
        self.assertIn('email', response.data)
        self.assertIn('token', response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
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
            data={"access_token": self.google_access_token}, format='json')
        self.assertEqual(json.loads(response.content), {"errors": {"provider":
                         ["This field is required."]}})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
