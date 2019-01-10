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
                "username": "Marygigz",
                "email": "jake@jake.jake",
                "password": "g@_Gigz-2416"
                }}
        self.login_data = {
            "user": {
                "email": "jake@jake.jake",
                "password": "g@_Gigz-2416"
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
                "password": "g@_Gigz-2416"
                }}
        self.signup_empty_email = {
            "user": {
                "username": "Marygigz",
                "email": "",
                "password": "g@_Gigz-2416"
                }}
        self.signup_empty_password = {
            "user": {
                "username": "Marygigz",
                "email": "jake@andela.com",
                "password": ""
                }}
        self.signup1 = {
            "user": {
                "username": "Marygigz",
                "email": "jake@jake.jake",
                "password": "g@_Gigz-2416"
                }}
        self.signup2 = {
            "user": {
                "username": "Maryjake",
                "email": "jake@andela.com",
                "password": "g@_Gigz-2416"
                }}
        self.signup3 = {
            "user": {
                "username": "Maryjake",
                "email": "jakey@andela.com",
                "password": "g@_Gigz-2416"
                }}
        self.duplicate_email = {
            "user": {
                "username": "Gigzjake",
                "email": "jacky@andela.com",
                "password": "g@_Gigz-2416"
                }}
        self.duplicate_email2 = {
            "user": {
                "username": "jacky2gigz",
                "email": "jacky@andela.com",
                "password": "g@_Gigz-2416"
                }}
        self.username_characters_only = {
                                            "user": {
                                                "username": "#@##@#@##@#",
                                                "email": "jake@jake.jake",
                                                "password": "g@AHJA473"
                                                }}
        self.username_number_only = {
                                            "user": {
                                                "username": "123455",
                                                "email": "jake@jake.jake",
                                                "password": "g@AHJA473"
                                                }}
        self.username_less_than_six = {
                                            "user": {
                                                "username": "Mary",
                                                "email": "jake@jake.jake",
                                                "password": "g@AHJA473"
                                            }}
        self.invalid_password = {
                                            "user": {
                                                "username": "MaryWnaja",
                                                "email": "jake1@jake.jake",
                                                "password": "gmnbjhggu"
                                            }}
        self.invalid_password_less_characters = {
                                            "user": {
                                                    "username": "MaryWnaja",
                                                    "email": "jake1@jake.jake",
                                                    "password": "@Maty1"
                                                }} 

    def test_register_user(self):
        """Test register user"""
        response = self.client.post(self.signup_url, self.signup_data,
                                    format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.content, b'{"user": {"email": "jake@jake.jake", "username": "Marygigz"}}')

    def test_empty_username(self):
        """Test register user with empty username"""
        response = self.client.post(self.signup_url,
                                    self.signup_empty_username,
                                    format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(json.loads(response.content), {"errors": {"username":
                                                        ["This field may not"
                                                            " be blank."]}})

    def test_empty_email(self):
        """Test register user with an empty email"""
        response = self.client.post(self.signup_url,
                                    self.signup_empty_email,
                                    format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(json.loads(response.content), {"errors":
                                                        {"email":
                                                         ["This field may not "
                                                          "be blank."]}})

    def test_empty_password(self):
        """Test register user with an empty password"""
        response = self.client.post(self.signup_url,
                                    self.signup_empty_password,
                                    format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(json.loads(response.content),  {"errors":
                                                         {"password":
                                                          ["This field may not"
                                                           " be blank."]}})

    def test_register_duplicate_email(self):
        """Test register user with a duplicate email"""
        self.client.post(self.signup_url,
                         self.duplicate_email,
                         format="json")
        response = self.client.post(self.signup_url,
                                    self.duplicate_email2,
                                    format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(json.loads(response.content), {"errors": {"email":
                                                        ["user with this email"
                                                         " already exists."]}})

    def test_register_duplicate_username(self):
        """Test register user with a duplicate email"""
        self.client.post(self.signup_url, self.signup2, format="json")
        response = self.client.post(self.signup_url, self.signup3,
                                    format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(json.loads(response.content), {"errors": {"username":
                                                        ["user with this"
                                                         " username already"
                                                         " exists."]}})

    def test_username_special_characters_only(self):
        """Test user details with username contaning characters only."""
        response = self.client.post(self.signup_url,
                                    self.username_characters_only,
                                    format="json")
        self.assertEqual(json.loads(response.content), {'errors':
                                                        {'username':
                                                         ['Username should not'
                                                          ' contain special'
                                                          ' character']}})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_username_numbers_only(self):
        """Test user details with username contaning numbers only."""
        response = self.client.post(self.signup_url,
                                    self.username_number_only, format="json")
        self.assertEqual(json.loads(response.content), {'errors': {'username':
                         ['Username should not contain numbers only']}})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_username_characters_less_than_six(self):
        """Test user details with username with less than six characters."""
        response = self.client.post(self.signup_url,
                                    self.username_less_than_six, format="json")
        self.assertEqual(json.loads(response.content), {'errors': {'username':
                         ['Username should have atleast 6 characters']}})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_invalid_password(self):
        """Test user details with invalid password."""
        response = self.client.post(self.signup_url,
                                    self.invalid_password, format="json")
        self.assertEqual(json.loads(response.content), {'errors': {'password':  
                         ['password should contain a lowercase, '
                          'uppercase numeric and special character']}})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_invalid_password_less_characters(self):
        """Test user details with password less than 6 characters."""
        response = self.client.post(self.signup_url,
                                    self.invalid_password_less_characters,
                                    format="json")
        self.assertEqual(json.loads(response.content), {'errors': {'password': 
                         ['Ensure Password field has at least 8 characters']}})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
