import json
from django.urls import reverse
from rest_framework.views import status
from rest_framework.test import APITestCase, APIClient


class RegistrationTestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.login_url = reverse('authentication:auth-login')
        self.signup_url = reverse('authentication:auth-register')
        self.signup_data = {
            "user": {
                "username": "gigz",
                "email": "jake@jake.jake",
                "password": "jakejake"
                }}
        self.login_data = {
            "user": {
                "email": "jake@jake.jake",
                "password": "jakejake"
                }}
        self.login_unregistered_user_data = {
            "user": {
                "email": "muinde@jake.jake",
                "password": "jakejake"
                }}
        self.signup_empty_username = {
            "user": {
                "username": "",
                "email": "jake@jake.jake",
                "password": "jakejake"
                }}
        self.signup_empty_email = {
            "user": {
                "username": "gigz",
                "email": "",
                "password": "jakejake"
                }}
        self.signup_empty_password = {
            "user": {
                "username": "gigz",
                "email": "jake@andela.com",
                "password": ""
                }}
        self.signup1 = {
            "user": {
                "username": "gigz",
                "email": "jake@andela.com",
                "password": "jakejake"
                }}
        self.signup2 = {
            "user": {
                "username": "jake",
                "email": "jake@andela.com",
                "password": "jakejake"
                }}
        self.signup3 = {
            "user": {
                "username": "jake",
                "email": "jakey@andela.com",
                "password": "jakejake"
                }}
        self.duplicate_email = {
            "user": {
                "username": "jake",
                "email": "jacky@andela.com",
                "password": "jakejake"
                }}
        self.duplicate_email2 = {
            "user": {
                "username": "jacky2",
                "email": "jacky@andela.com",
                "password": "jakejake"
                }}
                
    def test_register_user(self):
        ''''Test register user'''
        response = self.client.post(self.signup_url, self.signup_data,
                                    format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_empty_username(self):
        '''Test register user with empty username'''
        response = self.client.post(self.signup_url,
                                    self.signup_empty_username,
                                    format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(json.loads(response.content), {"errors": {"username":
                                                        ["This field may not be blank."]}})

    def test_empty_email(self):
        '''Test register user with an empty email'''
        response = self.client.post(self.signup_url,
                                    self.signup_empty_email,
                                    format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(json.loads(response.content), {"errors":
                                                        {"email":
                                                         ["This field may not be blank."]}})

    def test_empty_password(self):
        '''Test register user with an empty password'''
        response = self.client.post(self.signup_url,
                                    self.signup_empty_password,
                                    format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(json.loads(response.content),  {"errors":
                                                         {"password":
                                                          ["This field may not be blank."]}})

    def test_register_duplicate_email(self):
        '''Test register user with a duplicate email'''
        self.client.post(self.signup_url,
                         self.duplicate_email,
                         format="json")
        response = self.client.post(self.signup_url,
                                    self.duplicate_email2,
                                    format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(json.loads(response.content), {"errors": {"email":
                                                        ["user with this email already exists."]}})
    
    def test_register_duplicate_username(self):
        '''Test register user with a duplicate email'''
        self.client.post(self.signup_url, self.signup2, format="json")
        response = self.client.post(self.signup_url, self.signup3,
                                    format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(json.loads(response.content), {"errors": {"username":
                                                        ["user with this username already exists."]}})
