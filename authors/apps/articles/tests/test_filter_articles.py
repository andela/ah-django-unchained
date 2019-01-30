from django.urls import reverse
from rest_framework.views import status
from rest_framework.test import APITestCase, APIClient


class FilterArticles(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.sign_up_url = reverse('authentication:auth-register')
        self.filter_title_url = 'http://127.0.0.1:8000/api/article/search/?title=Coding is cool'
        self.filter_tag_url = 'http://127.0.0.1:8000/api/article/search/?tags=python'
        self.filter_all = 'http://127.0.0.1:8000/api/article/search/?tags=python&title=Coding is cool&author=Ken123'
        self.sign_up_data = {
            "user": {
                "username": "Ken123",
                "email": "kenisme@andela.com",
                "password": "Pass@123"
            }
        }
        self.article_listcreate_url = reverse('articles:articles-listcreate')
        self.article_data = {
            "title": "Coding is cool",
            "description": "Its cool",
            "body": "Django is interesting",
            "tagList": ["python"]
        }

    def register(self):
        """Sign up new user"""
        register = self.client.post(self.sign_up_url, self.sign_up_data,
                                    format='json')
        token = register.data['token']
        return token

    def test_filter_article_title(self):
        """Test that you can filter an article with a certain title."""

        token = self.register()
        # Create article
        self.client.post(self.article_listcreate_url, self.article_data,
                                    format='json',
                                    HTTP_AUTHORIZATION='token {}'.format(token)
                                    )
        response = self.client.get(self.filter_title_url,
                        format='json', HTTP_AUTHORIZATION='token {}'.format(token))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn(self.article_data['title'],response.data['results'][0]['title'])

    def test_filter_article_tag(self):
        """Test that you can filter an article with a specific tag"""

        token = self.register()
        # Create article
        self.client.post(self.article_listcreate_url, self.article_data,
                                    format='json',
                                    HTTP_AUTHORIZATION='token {}'.format(token)
                                    )
        response = self.client.get(self.filter_tag_url,
                        format='json', HTTP_AUTHORIZATION='token {}'.format(token))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertListEqual(self.article_data['tagList'],response.data['results'][0]['tagList'])

    def test_filter_all(self):
        """Test that you can filter an article with a specific title,taglist and author all at once """

        token = self.register()
        # Create article
        self.client.post(self.article_listcreate_url, self.article_data,
                                    format='json',
                                    HTTP_AUTHORIZATION='token {}'.format(token)
                                    )
        response = self.client.get(self.filter_all,
                        format='json', HTTP_AUTHORIZATION='token {}'.format(token))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn(self.article_data['title'], response.data['results'][0]['title'])
        self.assertListEqual(self.article_data['tagList'], response.data['results'][0]['tagList'])

