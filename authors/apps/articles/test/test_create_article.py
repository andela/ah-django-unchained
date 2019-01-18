import json
from django.urls import reverse
from rest_framework.views import status
from rest_framework.test import APITestCase, APIClient
# from ..models import User
# from ..models import Articles
from authors.apps.articles.models import Article
# from authors.apps.authentication.views import LoginAPIView, RegistrationAPIView

class CreateArticles(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.login_url = reverse('authentication:auth-login')
        self.signup_url = reverse('authentication:auth-register')
        self.listcreate = reverse('articles:articles-listcreate')
        self.signup_data = {
            "user": {
                "username": "kennyg",
                "email": "ken@me.com",
                "password": "Kennyisme1!"
                }}
        self.login_data = {
            "user": {
                "email": "ken@me.com",
                "password": "Kennyisme1!"
                }}
        self.signup_data2 = {
            "user": {
                "username": "kwammea",
                "email": "kwame@me.com",
                "password": "Kwameisme1!"
                }}
        self.create_article_data = {
            "title": "A new story",
            "body": "This is my story",
            "description": "Here is my story",
            "images": None
        }
        self.create_article_data2 = {
            "title": "The beginning",
            "body": "This begins nowy",
            "description": "Here is my story",
            "images": None
        }
        self.delete_article = {
            "is_displayed": False
        }

    def test_fetch_all_articles(self):
        """Tests to fetch all articles"""
        register = self.client.post(self.signup_url,
                                    self.signup_data,
                                    format='json')
        token = register.data['token']
        del self.create_article_data['images']
        response = self.client.post(self.listcreate,
                                    self.create_article_data, format='json',
                                    HTTP_AUTHORIZATION='token {}'.format(token))
        response = self.client.post(self.listcreate,
                                    self.create_article_data, format='json',
                                    HTTP_AUTHORIZATION='token {}'.format(token))
        response = self.client.get(self.listcreate, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_add_articles(self):
        """Test to add an article"""
        register = self.client.post(self.signup_url,
                                    self.signup_data,
                                    format='json')
        token = register.data['token']
        del self.create_article_data['images']
        response = self.client.post(self.listcreate,
                                    self.create_article_data, format='json',
                                    HTTP_AUTHORIZATION='token {}'.format(token))
        self.assertEqual(register.status_code, status.HTTP_201_CREATED)
        self.assertIn("title", response.data)
        self.assertIn("body", response.data)
        self.assertIn("description", response.data)

    def test_get_single_article(self):
        """Test to get a single article"""
        register = self.client.post(self.signup_url,
                                    self.signup_data,
                                    format='json')
        token = register.data['token']
        del self.create_article_data['images']
        response = self.client.post(self.listcreate,
                                    self.create_article_data, format='json',
                                    HTTP_AUTHORIZATION='token {}'.format(token))
        self.assertEqual(register.status_code, status.HTTP_201_CREATED)
        response = self.client.get(reverse('articles:articles-retrieveupdate', kwargs={'slug': 'a-new-story'}), format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("title", response.data)
        self.assertIn("body", response.data)
        self.assertIn("description", response.data)

    def test_unauthorized_article_update(self):
        """Test to update an article created by another user"""
        register = self.client.post(self.signup_url,
                                    self.signup_data,
                                    format='json')
        token = register.data['token']
        del self.create_article_data['images']
        response = self.client.post(self.listcreate,
                                    self.create_article_data, format='json',
                                    HTTP_AUTHORIZATION='token {}'.format(token))
        register = self.client.post(self.signup_url,
                                    self.signup_data2,
                                    format='json')
        token = register.data['token']
        response = self.client.put(reverse('articles:articles-retrieveupdate', kwargs={'slug': 'a-new-story'}),
                                    self.create_article_data2, format='json',
                                    HTTP_AUTHORIZATION='token {}'.format(token))
        self.assertAlmostEquals(response.status_code, status.HTTP_403_FORBIDDEN)
    
    def test_authorized_article_update(self):
        """Test to legitimately update an article created by a user"""
        register = self.client.post(self.signup_url,
                                    self.signup_data,
                                    format='json')
        token = register.data['token']
        del self.create_article_data['images']
        response = self.client.post(self.listcreate,
                                    self.create_article_data, format='json',
                                    HTTP_AUTHORIZATION='token {}'.format(token))
        del self.create_article_data2['images']
        response = self.client.put(reverse('articles:articles-retrieveupdate', kwargs={'slug': 'a-new-story'}),
                                    self.create_article_data2, format='json',
                                    HTTP_AUTHORIZATION='token {}'.format(token))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
