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
        profile = self.client.get(reverse('profiles:get-profile', kwargs={'slug': 'johndoe'}),format='json')
        self.assertEqual(self.profile_data,profile.data)
    
    def test_post_profile(self):
            """Test post profile upon registrations"""
            self.profile_data['first_name'],self.profile_data['last_name'] = 'kwame', 'asiago'
            self.profile_data['bio'] = 'some bio'
            del self.profile_data['profile_image']
            register = self.client.post(self.signup_url,self.signup_data,format='json')
            self.assertEqual(register.status_code, status.HTTP_201_CREATED)
            token  = register.data['token']
            profile = self.client.put(reverse('profiles:post-profile', kwargs={'slug': 'johndoe'}),self.profile_data,
            format='json',HTTP_AUTHORIZATION='token {}'.format(token))
            self.profile_data['profile_image'] = None
            self.assertEqual(self.profile_data,profile.data)