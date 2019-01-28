import os
from django.urls import reverse
from rest_framework.views import status
from rest_framework.test import APITestCase, APIClient


class CreateArticles(APITestCase):

    def setUp(self):
        self.client = APIClient()
        self.signup_url = reverse('authentication:auth-register')
        self.article_listcreate = reverse('articles:articles-listcreate')
        self.base_url = os.getenv('APP_BASE_URL')
        self.share_mail_url = self.base_url + \
            '/api/articles/a-new-story/share/email/?email=bevstop@gmail.com'
        self.invalid_mail_url = self.base_url + \
            '/api/articles/a-new-story/share/email/?email=bevstopgmail.com'

        self.signup_data = {
            "user": {
                "username": "kennyg",
                "email": "ken@me.com",
                "password": "Kennyisme1!"
            }}
        self.create_article_data = {
            "title": "A new story",
            "body": "This is my story",
            "description": "Here is my story",
            "images": None,
            "tagList": ["dragons", "training"]
        }

    def signup_user_one(self):
        """Function to register user one and return their token"""
        register = self.client.post(self.signup_url,
                                    self.signup_data,
                                    format='json')
        token = register.data['token']
        return token

    def create_article(self, article, token):
        """Function to create an article"""
        del article['images']
        response = self.client.post(self.article_listcreate,
                                    article,
                                    format='json',
                                    HTTP_AUTHORIZATION='token {}'.format(token))
        return response

    def test_facebook_share(self):
        """Test to share via facebook"""
        token = self.signup_user_one()
        self.create_article(self.create_article_data, token)
        response = self.client.get(reverse('articles:share_facebook',
                                           kwargs={'slug': 'a-new-story'}),
                                   format='json',
                                   HTTP_AUTHORIZATION='token {}'.format(token))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['link'],
                         'https://www.facebook.com/sharer/sharer.php?u='
                         + self.base_url + '/api/articles/a-new-story')

    def test_twitter_share(self):
        """Test to share via twitter"""
        token = self.signup_user_one()
        self.create_article(self.create_article_data, token)
        response = self.client.get(reverse('articles:share_twitter',
                                           kwargs={'slug': 'a-new-story'}),
                                   format='json',
                                   HTTP_AUTHORIZATION='token {}'.format(token))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['link'],
                         'https://twitter.com/home?status=Check%20this%20out%20'
                         + self.base_url + '/api/articles/a-new-story')

    def test_missing_article_facebook(self):
        """test to share a missing article on facebook"""
        token = self.signup_user_one()
        self.create_article(self.create_article_data, token)
        response = self.client.get(reverse('articles:share_facebook',
                                           kwargs={'slug': 'a-newer-story'}),
                                   format='json',
                                   HTTP_AUTHORIZATION='token {}'.format(token))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data['detail'],
                         "This article does not exist")

    def test_missing_article_twitter(self):
        """test to share a missing article on twitter"""
        token = self.signup_user_one()
        self.create_article(self.create_article_data, token)
        response = self.client.get(reverse('articles:share_twitter',
                                           kwargs={'slug': 'a-newer-story'}),
                                   format='json',
                                   HTTP_AUTHORIZATION='token {}'.format(token))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data['detail'],
                         "This article does not exist")

    def test_email_share(self):
        """Test to share via email"""
        token = self.signup_user_one()
        self.create_article(self.create_article_data, token)
        response = self.client.get(self.share_mail_url, format='json',
                                   HTTP_AUTHORIZATION='token {}'.format(token))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data['message'], "Article link sent successfully.")

    def test_missing_article_email(self):
        """test to share a missing article on email"""
        token = self.signup_user_one()
        response = self.client.get(self.share_mail_url, format='json',
                                   HTTP_AUTHORIZATION='token {}'.format(token))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data['errors']
                         ['message'][0], "Article not found.")

    def test_share_without_email(self):
        """test to share an article without providing email"""
        token = self.signup_user_one()
        self.create_article(self.create_article_data, token)
        response = self.client.get(reverse('articles:share_email',
                                           kwargs={'slug': 'a-new-story'}),
                                   format='json', HTTP_AUTHORIZATION='token {}'.format(token))
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['errors'], {
            "email": [
                "Email not provided."
            ]})

    def test_invalid_email(self):
        """test to share an article with an invalid email"""
        token = self.signup_user_one()
        self.create_article(self.create_article_data, token)
        response = self.client.get(self.invalid_mail_url, format='json',
                                   HTTP_AUTHORIZATION='token {}'.format(token))
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['message'],
                         "The email provided is not a valid one."
                         )
