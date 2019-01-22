import json
from django.urls import reverse
from rest_framework.views import status
from rest_framework.test import APITestCase, APIClient
from authors.apps.articles.models import Article


class CreateArticles(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.login_url = reverse('authentication:auth-login')
        self.signup_url = reverse('authentication:auth-register')
        self.article_listcreate = reverse('articles:articles-listcreate')
        self.signup_data = {
            "user": {
                "username": "kennyg",
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
            "body": "This begins now",
            "description": "Here is my story",
            "images": None
        }
        self.delete_article = {
            "is_deleted": True
        }

    def signup_user_one(self):
        """Function to register user one and return their token"""
        register = self.client.post(self.signup_url,
                                    self.signup_data,
                                    format='json')
        token = register.data['token']
        return token

    def signup_user_two(self):
        """Function to register user two and return their token"""
        register = self.client.post(self.signup_url,
                                    self.signup_data2,
                                    format='json')
        token = register.data['token']
        return token

    def test_fetch_all_articles(self):
        """Tests to fetch all articles"""
        token = self.signup_user_one()
        del self.create_article_data['images']
        self.client.post(self.article_listcreate,
                         self.create_article_data,
                         format='json',
                         HTTP_AUTHORIZATION='token {}'.format(token))
        del self.create_article_data2['images']
        self.client.post(self.article_listcreate,
                         self.create_article_data2,
                         format='json',
                         HTTP_AUTHORIZATION='token {}'.format(token))
        response = self.client.get(self.article_listcreate, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.create_article_data['title'],
                         response.data[0]['title'])
        self.assertEqual(self.create_article_data2['title'],
                         response.data[1]['title'])
        self.assertEqual(self.create_article_data['body'],
                         response.data[0]['body'])
        self.assertEqual(self.create_article_data2['body'],
                         response.data[1]['body'])
        self.assertEqual(self.create_article_data['description'],
                         response.data[0]['description'])
        self.assertEqual(self.create_article_data2['description'],
                         response.data[1]['description'])

    def test_add_articles(self):
        """Test to add an article"""
        token = self.signup_user_one()
        del self.create_article_data['images']
        response = self.client.post(self.article_listcreate,
                                    self.create_article_data,
                                    format='json',
                                    HTTP_AUTHORIZATION='token {}'.format(token))
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(self.create_article_data['title'],
                         response.data['title'])
        self.assertEqual(self.create_article_data['body'],
                         response.data['body'])
        self.assertEqual(self.create_article_data['description'],
                         response.data['description'])

    def test_get_single_article(self):
        """Test to get a single article"""
        token = self.signup_user_one()
        del self.create_article_data['images']
        self.client.post(self.article_listcreate,
                         self.create_article_data,
                         format='json',
                         HTTP_AUTHORIZATION='token {}'.format(token))
        response = self.client.get(reverse('articles:articles-retrieveupdate',
                                   kwargs={'slug': 'a-new-story'}),
                                   format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.create_article_data['title'],
                         response.data['title'])
        self.assertEqual(self.create_article_data['body'],
                         response.data['body'])
        self.assertEqual(self.create_article_data['description'],
                         response.data['description'])

    def test_unauthorized_article_update(self):
        """Test to update an article created by another user"""
        token = self.signup_user_one()
        del self.create_article_data['images']
        self.client.post(self.article_listcreate,
                         self.create_article_data,
                         format='json',
                         HTTP_AUTHORIZATION='token {}'.format(token))
        token2 = self.signup_user_two()
        response = self.client.put(reverse('articles:articles-retrieveupdate',
                                   kwargs={'slug': 'a-new-story'}),
                                   self.create_article_data2,
                                   format='json',
                                   HTTP_AUTHORIZATION='token {}'.format(token2))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_authorized_article_update(self):
        """Test to legitimately update an article created by a user"""
        token = self.signup_user_one()
        del self.create_article_data['images']
        self.client.post(self.article_listcreate,
                         self.create_article_data,
                         format='json',
                         HTTP_AUTHORIZATION='token {}'.format(token))
        del self.create_article_data2['images']
        response = self.client.put(reverse('articles:articles-retrieveupdate',
                                   kwargs={'slug': 'a-new-story'}),
                                   self.create_article_data2,
                                   format='json',
                                   HTTP_AUTHORIZATION='token {}'.format(token))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.create_article_data2['title'],
                         response.data['title'])
        self.assertEqual(self.create_article_data2['body'],
                         response.data['body'])
        self.assertEqual(self.create_article_data2['description'],
                         response.data['description'])

    def test_to_delete_article(self):
        """Test to delete an article"""
        token = self.signup_user_one()
        del self.create_article_data['images']
        self.client.post(self.article_listcreate,
                         self.create_article_data,
                         format='json',
                         HTTP_AUTHORIZATION='token {}'.format(token))
        response = self.client.put(reverse('articles:articles-delete',
                                   kwargs={'slug': 'a-new-story'}),
                                   self.delete_article,
                                   format='json',
                                   HTTP_AUTHORIZATION='token {}'.format(token))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_unauthorized_delete_article(self):
        """Test to delete someone else's article"""
        token = self.signup_user_one()
        del self.create_article_data['images']
        self.client.post(self.article_listcreate,
                         self.create_article_data,
                         format='json',
                         HTTP_AUTHORIZATION='token {}'.format(token))
        token2 = self.signup_user_two()
        response = self.client.put(reverse('articles:articles-delete',
                                   kwargs={'slug': 'a-new-story'}),
                                   self.delete_article,
                                   format='json',
                                   HTTP_AUTHORIZATION='token {}'.format(token2))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual('You are not allowed to edit or delete this object',
                         response.data['detail'])

    def test_to_fetch_non_exisiting_article(self):
        """Test to fetch an article that does not exist"""
        response = self.client.get(reverse('articles:articles-retrieveupdate',
                                   kwargs={'slug': 'a-new-story'}),
                                   format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual('Not found', response.data['detail'])
