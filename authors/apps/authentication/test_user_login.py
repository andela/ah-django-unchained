import json
from django.urls import reverse
from rest_framework.views import status
from rest_framework.test import APITestCase,APIClient

# from authors.apps.authentication.backends import JWTAuthentication
# 
class LoginTestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.login_url =reverse('authentication:auth-login')
        self.signup_data = {
            "username":"gigz",
            "email": "jake@jake.jake",
            "password": "jakejake"
            }
        self.login_data = {
            "email": "jake@jake.jake",
            "password": "jakejake"
            }
        self.login_unregistered_user_data = {
            "email": "jake@jake.jake",
            "password": "jakejake"
            }
        
        self.token={'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9'}

    def test_login(self):
        ''' if user is registered'''
        register=self.client.post(self.login_url,
            self.signup_data,
            format="json")
        
        self.assertEqual(register.status_code, status.HTTP_201_CREATED)
        
        '''Test login'''

        response= self.client.post(self.login_url,
        self.login_data,format="json")
        self.assertEqual(response.status_code, status.HTT0_200_OK)
        self.assertIn(b"Successfully Logged in",response.content)
    
    def test_login_unregistered_user(self):
        '''Test login for unregistered users'''
        response = self.client.post(self.login_url,self.login_unregistered_user_data)
        self.assertEqual(response.status_code,status.HTTP_401_UNAUTHORIZED)

