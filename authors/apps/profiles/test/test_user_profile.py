import json
from django.urls import reverse
from rest_framework.views import status
from rest_framework.test import APITestCase, APIClient


class LoginTestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.login_url = reverse('authentication:auth-login')
        self.signup_url = reverse('authentication:auth-register')
        self.data_john = {
            "user": {
                "username": "johndoe",
                "email": "john@gmail.com",
                "password": "@Qwerty12345"
            }}
        self.data_jane = {
            "user": {
                "username": "janedoe",
                "email": "jane@gmail.com",
                "password": "@Qwerty12345"
            }}
        self.profile_data = {
            "first_name": "kwame",
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

    def register_user(self, user):
        register = self.client.post(
            self.signup_url, user, format='json')
        return register.data['token']

    def test_get_user_profile(self):
        """Test get profile upon registrations"""
        self.register_user(self.data_john)
        # get user profile
        profile = self.client.get(
            reverse('profiles:put-profile', kwargs={'username': self.data_john['user']['username']}), format='json')
        self.assertEqual(profile.status_code, status.HTTP_200_OK)

    def test_updating_profile(self):
        """Test updating profile upon registrations"""
        token = self.register_user(self.data_john)
        # update profile
        profile = self.client.put(reverse('profiles:put-profile',
                                          kwargs={'username': self.data_john['user']['username']}),
                                  self.profile_data, format='json', HTTP_AUTHORIZATION='token {}'.format(token))
        self.assertEqual(profile.status_code, status.HTTP_200_OK)
        self.assertEqual(
            profile.data, {'message': 'Profile has been updated successfully'})

    def test_updating_invalid_gender(self):
        """Test updating an invalid gender"""
        token = self.register_user(self.data_john)
        # update profile
        profile = self.client.put(
            reverse(
                'profiles:put-profile',
                kwargs={'username': self.data_john['user']['username']}),
            self.invalid_gender,
            format='json',
            HTTP_AUTHORIZATION='token {}'.format(token))
        self.assertEqual(profile.status_code, status.HTTP_400_BAD_REQUEST)
        msg = 'Please enter M if you are male, F if you are female or N if you do not want to disclose'
        data = {'errors': {'gender': [msg]}}
        self.assertEqual(data, json.loads(profile.content))

    def test_updating_invalid_user(self):
        """Test updating with other peaople user profile"""
        self.register_user(self.data_jane)
        token = self.register_user(self.data_john)
        profile = self.client.put(
            reverse(
                'profiles:put-profile',
                kwargs={'username': self.data_jane['user']['username']}),
            self.invalid_gender,
            format='json',
            HTTP_AUTHORIZATION='token {}'.format(token))
        self.assertEqual(profile.status_code, status.HTTP_403_FORBIDDEN)
        data = {'error': 'You are not allowed to edit or delete this object'}
        self.assertEqual(data, json.loads(profile.content))

    def test_non_existing_user(self):
        """Test updating an user that does not exist"""
        token = self.register_user(self.data_jane)
        # update profile
        profile = self.client.put(
            reverse(
                'profiles:put-profile',
                kwargs={'username': 'noneExist'}),
            self.profile_data,
            format='json',
            HTTP_AUTHORIZATION='token {}'.format(token))
        self.assertEqual(profile.status_code, status.HTTP_404_NOT_FOUND)
        data = {'error': 'Username noneExist not found'}
        self.assertEqual(data, json.loads(profile.content))
