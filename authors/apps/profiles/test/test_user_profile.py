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
            "first_name": "kwame",
            "last_name": "asiago",
            "gender": "F",
            "bio": "my bio"
        }
        self.empty_first_name = {
            "first_name": "",
            "last_name": "asiago",
            "gender": "F",
            "bio": "my bio"
        }
        self.invalid_gender = {
            "first_name": "kwame",
            "last_name": "asiago",
            "gender": "G",
            "bio": "my bio"
        }

    def get_token(self):
        register = self.client.post(
            self.signup_url, self.signup_data, format='json')
        self.assertEqual(register.status_code, status.HTTP_201_CREATED)
        return register.data['token']


    def test_get_user_profile(self):
        """Test get profile upon registrations"""
        # register user
        register = self.client.post(
            self.signup_url, self.signup_data, format='json')
        self.assertEqual(register.status_code, status.HTTP_201_CREATED)

        # get user profile
        profile = self.client.get(
            reverse('profiles:put-profile', kwargs={'username': 'johndoe'}), format='json')
        self.assertEqual(profile.status_code, status.HTTP_200_OK)

    def test_updating_profile(self):
        """Test post profile upon registrations"""
        token = self.get_token()
        # update profile
        profile = self.client.put(reverse('profiles:put-profile', kwargs={'username': 'johndoe'}),
                                  self.profile_data, format='json', HTTP_AUTHORIZATION='token {}'.format(token))
        self.assertEqual(profile.status_code, status.HTTP_200_OK)
        self.assertEqual(
            profile.data, {'response': 'profile has been updated successfully '})

    def test_updating_empty_first_name(self):
        """Test post profile upon registrations"""
        token = self.get_token()
        # update profile
        profile = self.client.put(
            reverse(
                'profiles:put-profile',
                kwargs={'username': 'johndoe'}
                ),
            self.empty_first_name, format='json',
            HTTP_AUTHORIZATION='token {}'.format(token))
        self.assertEqual(profile.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            {'errors': {'first_name': [
                         'This field may not be blank.']}},
            json.loads(profile.content))

    def test_updating_invalid_gender(self):
        """Test post profile upon registrations"""
        token = self.get_token()
        # update profile
        profile = self.client.put(
            reverse(
                'profiles:put-profile',
                kwargs={'username': 'johndoe'}),
            self.invalid_gender,
            format='json',
            HTTP_AUTHORIZATION='token {}'.format(token))
        self.assertEqual(profile.status_code, status.HTTP_400_BAD_REQUEST)
        msg = 'Please enter M if you are male, F if you are female or N if you do not want to disclose '
        data = {'errors': {'gender': [msg]}}
        self.assertEqual(data, json.loads(profile.content))
