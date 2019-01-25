import json
from django.urls import reverse
from rest_framework.views import status
from rest_framework.test import APITestCase, APIClient


class CommentsTestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.login_url = reverse('authentication:auth-login')
        self.signup_url = reverse('authentication:auth-register')
        self.article_listcreate = reverse('articles:articles-listcreate')
        self.comments_url = '/api/articles/my-story/comments/'
        self.comments_url_nonexistant_article = '/api/articles/mystory/comments/'
        self.get_comment_url = '/api/articles/my-story/comments/1/'

        self.signup_data = {
                        "user": {
                            "username": "maggie123",
                            "email": "margaret.chege@andela.com",
                            "password": "Pass@123"
                        }
                        }
        self.login_data = {"user": {
                        "email": "margaret1.chege@andela.com",
                        "password": "Pass@123"
                    }}
        self.new_comment = {
            "body": "Good Work"
            }
        self.update_comment = {
            "body": "This is super cool"
            }
        self.empty_comment = {
            "body": ""
            }
        self.create_article_data = {
            "title": "my story",
            "body": "This is my story",
            "description": "Here is my story",
            "images": None
        }

    def register(self):
        """Sign up user and get token"""
        register = self.client.post(self.signup_url,
                                    self.signup_data,
                                    format='json')
                                
        token = register.data["token"]
        return token

    def create_article(self):
        token = self.register()
        del self.create_article_data['images']
        response = self.client.post(self.article_listcreate,
                                    self.create_article_data,
                                    format='json',
                                    HTTP_AUTHORIZATION='token {}'.format(token)
                                    )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        return response

    def test_create_comment_on_article(self):
        token = self.register()
        del self.create_article_data['images']
        response = self.client.post(self.article_listcreate,
                                    self.create_article_data,
                                    format='json',
                                    HTTP_AUTHORIZATION='token {}'.format(token)
                                    )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        return response
        response = self.client.post(self.comments_url,
                                    self.new_comment,
                                    format='json',
                                    HTTP_AUTHORIZATION='token {}'.format(token)
                                    )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_comment_for_unregisterd_user(self):
        self.create_article()
        response = self.client.post(self.comments_url,
                                    self.new_comment,
                                    format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(
            json.loads(response.content),
            {'detail': 'Authentication credentials were not provided.'}
            )

    def test_create_comment_nonexistent_article(self):
        token = self.register()
        del self.create_article_data['images']
        response = self.client.post(self.article_listcreate,
                                    self.create_article_data,
                                    format='json',
                                    HTTP_AUTHORIZATION='token {}'.format(token)
                                    )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        return response
        response = self.client.post(self.comments_url_nonexistant_article,
                                    self.new_comment,
                                    format='json',
                                    HTTP_AUTHORIZATION='token {}'.format(token)
                                    )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(json.loads(response.content), {'detail': 'Not found'})




