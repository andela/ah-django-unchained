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

        self.new_comment = {
            "body": "Good Work"
        }
        self.update_comment = {
            "body": "This is super cool"
        }
        self.update_comment_2 = {
            "body": "This is super cool.Maaan!"
        }
        self.create_article_data = {
            "title": "my story",
            "body": "This is my story",
            "description": "Here is my story",
            "tagList": ["dragons", "training"]

        }

    def register(self):
        """Sign up user and get token"""
        register = self.client.post(self.signup_url,
                                    self.signup_data,
                                    format='json')

        token = register.data["token"]
        return token

    def create_article(self, article, token):
        response = self.client.post(self.article_listcreate,
                                    article,
                                    format='json',
                                    HTTP_AUTHORIZATION='token {}'.format(token))
        return response

    def test_create_comment_view_history(self):
        """Test Create Comment and view History"""
        token = self.register()
        self.create_article(self.create_article_data, token)
        response = self.client.post(reverse('articles:create_comments',
                                            kwargs={'slug': 'my-story'}),
                                    self.new_comment,
                                    format='json',
                                    HTTP_AUTHORIZATION='token {}'.format(token)
                                    )
        id = response.data['id']
        response = self.client.get(reverse("articles:comment_history",
                                           kwargs={'slug': 'my-story', "id": id}),
                                   format='json',
                                   HTTP_AUTHORIZATION='token {}'.format(token))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['comment_history']), 1)

    def test_update_comment_view_history(self):
        """Test Update Comment and view History"""
        token = self.register()
        self.create_article(self.create_article_data, token)
        response = self.client.post(reverse('articles:create_comments',
                                            kwargs={'slug': 'my-story'}),
                                    self.new_comment,
                                    format='json',
                                    HTTP_AUTHORIZATION='token {}'.format(token)
                                    )
        id = response.data['id']
        self.client.put(reverse("articles:get_comments",
                                kwargs={'slug': 'my-story', "id": id}),
                        self.update_comment,
                        format='json',
                        HTTP_AUTHORIZATION='token {}'.format(token))
        self.client.put(reverse("articles:get_comments",
                                kwargs={'slug': 'my-story', "id": id}),
                        self.update_comment_2,
                        format='json',
                        HTTP_AUTHORIZATION='token {}'.format(token))
        response = self.client.get(reverse("articles:comment_history",
                                           kwargs={'slug': 'my-story', "id": id}),
                                   format='json',
                                   HTTP_AUTHORIZATION='token {}'.format(token))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['comment_history']), 3)

    def test_view_history_non_existent_comment(self):
        """Test to get comment history for non existent comment"""
        token = self.register()
        self.create_article(self.create_article_data, token)
        response = self.client.post(reverse('articles:create_comments',
                                            kwargs={'slug': 'my-story'}),
                                    self.new_comment,
                                    format='json',
                                    HTTP_AUTHORIZATION='token {}'.format(token)
                                    )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        response = self.client.get(reverse("articles:comment_history",
                                           kwargs={'slug': 'my-story', "id": 10909}),
                                   format='json',
                                   HTTP_AUTHORIZATION='token {}'.format(token))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data['error'],
                         'This comment does not exist')

    def test_view_history_non_existent_article(self):
        """Test Create Comment and view History"""
        token = self.register()
        self.create_article(self.create_article_data, token)
        response = self.client.post(reverse('articles:create_comments',
                                            kwargs={'slug': 'my-story'}),
                                    self.new_comment,
                                    format='json',
                                    HTTP_AUTHORIZATION='token {}'.format(token)
                                    )
        id = response.data['id']
        response = self.client.get(reverse("articles:comment_history",
                                           kwargs={'slug': 'four-oh-four', "id":id}),
                                   format='json',
                                   HTTP_AUTHORIZATION='token {}'.format(token))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data['detail'],
                         "This article does not exist")
