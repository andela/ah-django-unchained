import json
from django.urls import reverse
from rest_framework.views import status
from rest_framework.test import APITestCase, APIClient


class CommentsTestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.signup_url = reverse('authentication:auth-register')
        self.article_listcreate = reverse('articles:articles-listcreate')
        self.signup_data = {
                        "user": {
                            "username": "maggie123",
                            "email": "margaret.chege@andela.com",
                            "password": "Pass@123"
                        }
                        }
        self.reply_to_comment = {"comment": {
            "body": "Woow! Great work"
            }}

        self.new_comment = {
            "body": "Good Work"
            }
        self.update_comment = {
            "body": "This is super cool"
            }
        self.create_article_data = {
            "title": "my story",
            "body": "This is my story",
            "description": "Here is my story",
            "images": None,
            "tagList": ["dragons", "training"]

        }
        self.delete_comment = {
            "is_deleted": True
                }

    def register(self):
        """Sign up user and get token"""
        register = self.client.post(self.signup_url,
                                    self.signup_data,
                                    format='json')

        token = register.data["token"]
        return token

    def test_update_comment(self):
        """Test Update Comment"""
        token = self.register()
        del self.create_article_data['images']
        response = self.client.post(self.article_listcreate,
                                    self.create_article_data,
                                    format='json',
                                    HTTP_AUTHORIZATION='token {}'.format(token)
                                    )
        response = self.client.post(reverse('articles:create_comments',
                                    kwargs={'slug': 'my-story'}),
                                    self.new_comment,
                                    format='json',
                                    HTTP_AUTHORIZATION='token {}'.format(token)
                                    )
        id = response.data['id']
        response = self.client.put(reverse("articles:get_comments",
                                   kwargs={'slug': 'my-story', "id": id}),
                                   self.update_comment,
                                   format='json',
                                   HTTP_AUTHORIZATION='token {}'.format(token))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['body'], self.update_comment['body'])

    def test_reply_to_comment(self):
        """Test Update Comment"""

        token = self.register()
        """Create an article"""
        del self.create_article_data['images']
        response = self.client.post(self.article_listcreate,
                                    self.create_article_data,
                                    format='json',
                                    HTTP_AUTHORIZATION='token {}'.format(token)
                                    )
        """Create comment"""
        response = self.client.post(reverse('articles:create_comments',
                                    kwargs={'slug': 'my-story'}),
                                    self.new_comment,
                                    format='json',
                                    HTTP_AUTHORIZATION='token {}'.format(token)
                                    )
        id = response.data['id']
        response = self.client.post(reverse('articles:create_thread_comments',
                                    kwargs={'slug': 'my-story', 'id': id}),
                                    self.reply_to_comment,
                                    format='json',
                                    HTTP_AUTHORIZATION='token {}'.format(token)
                                    )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_single_comment(self):
        
        token = self.register()
        """Create an article"""
        del self.create_article_data['images']
        response = self.client.post(self.article_listcreate,
                                    self.create_article_data,
                                    format='json',
                                    HTTP_AUTHORIZATION='token {}'.format(token)
                                    )
        """Create comment"""
        response = self.client.post(reverse('articles:create_comments',
                                    kwargs={'slug': 'my-story'}),
                                    self.new_comment,
                                    format='json',
                                    HTTP_AUTHORIZATION='token {}'.format(token)
                                    )
        id = response.data['id']
        """Test get all comments"""
        response = self.client.get(reverse('articles:get_comments',
                                           kwargs={'slug': 'my-story', "id": id}),
                                   format='json',
                                   HTTP_AUTHORIZATION='token {}'.format(token))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_comment(self):
        token = self.register()
        """Create an article"""
        del self.create_article_data['images']
        response = self.client.post(self.article_listcreate,
                                    self.create_article_data,
                                    format='json',
                                    HTTP_AUTHORIZATION='token {}'.format(token)
                                    )
        """Create comment"""
        response = self.client.post(reverse('articles:create_comments',
                                    kwargs={'slug': 'my-story'}),
                                    self.new_comment,
                                    format='json',
                                    HTTP_AUTHORIZATION='token {}'.format(token)
                                    )
        id = response.data['id']
        """Test Delete a comment"""
        response = self.client.put(reverse('articles:delete_comments',
                                           kwargs={'slug': 'my-story', "id": id}),
                                   self.delete_comment,
                                   format='json',
                                   HTTP_AUTHORIZATION='token {}'.format(token))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_comment_on_article(self):
        """Register User"""
        token = self.register()
        del self.create_article_data['images']
        """Create an article"""
        response = self.client.post(self.article_listcreate,
                                    self.create_article_data,
                                    format='json',
                                    HTTP_AUTHORIZATION='token {}'.format(token)
                                    )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        """Create a comment"""
        response = self.client.post(reverse('articles:create_comments',
                                    kwargs={'slug': 'my-story'}),
                                    self.new_comment,
                                    format='json',
                                    HTTP_AUTHORIZATION='token {}'.format(token)
                                    )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_comment_for_unregistered_user(self):
        """Test Create a comment without registering a user."""
        token = self.register()
        response = self.client.post(self.article_listcreate,
                                    self.create_article_data,
                                    format='json',
                                    HTTP_AUTHORIZATION='token {}'.format(token)
                                    )
        response = self.client.post(reverse('articles:create_comments',
                                    kwargs={'slug': 'my-story'}),
                                    self.new_comment,
                                    format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(
            json.loads(response.content),
            {'detail': 'Authentication credentials were not provided.'}
            )

    def test_create_comment_nonexistent_article(self):
        """Create a comment for an article that doesn't exist"""
        token = self.register()
        response = self.client.post(reverse('articles:create_comments',
                                    kwargs={'slug': 'my-story1'}),
                                    self.new_comment,
                                    format='json',
                                    HTTP_AUTHORIZATION='token {}'.format(token)
                                    )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(json.loads(response.content), {'detail': 'Not found.'})
