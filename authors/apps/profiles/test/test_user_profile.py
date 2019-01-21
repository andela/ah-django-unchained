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
            "gender": "M",
            "bio": "my bio"
        }

    def test_get_user_profile(self):
        """Test get profile upon registrations"""
        # register user
        register = self.client.post(
            self.signup_url, self.signup_data, format='json')
        self.assertEqual(register.status_code, status.HTTP_201_CREATED)

        # get user profile
        profile = self.client.get(
            reverse('profiles:get-profile', kwargs={'slug': 'johndoe'}), format='json')
        self.assertEqual(register.status_code, status.HTTP_201_CREATED)

    def test_updating_profile(self):
        """Test post profile upon registrations"""
        # sign up a user and get token
        register = self.client.post(
            self.signup_url, self.signup_data, format='json')
        self.assertEqual(register.status_code, status.HTTP_201_CREATED)
        token = register.data['token']

        # update profile
        profile = self.client.put(reverse('profiles:post-profile', kwargs={'slug': 'johndoe'}), self.profile_data,
                                  format='json', HTTP_AUTHORIZATION='token {}'.format(token))
        self.profile_data['profile_image'] = None
        self.assertEqual(profile.status_code, status.HTTP_200_OK)
