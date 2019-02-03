from django.urls import reverse
from rest_framework.views import status
from rest_framework.test import APITestCase, APIClient
from urllib.parse import quote


class FilterArticles(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.author_filter = 'Ken123'
        self.sign_up_url = reverse('authentication:auth-register')
        self.article_listcreate = reverse('articles:articles-listcreate')
        title = quote('Coding is cool')
        self.filter_title_url = 'http://127.0.0.1:8000/api/articles/search/?title={}'.format(
            title)
        self.filter_tag_url = 'http://127.0.0.1:8000/api/articles/search/?tags=python'
        self.filter_author_url = 'http://127.0.0.1:8000/api/articles/search/?author={}'.format(
            self.author_filter)
        self.author_filter2 = 'MaggyC123'
        self.filter_all = 'http://127.0.0.1:8000/api/articles/search/?tags=python&title={}&author={}'.format(
            title, self.author_filter)
        self.sign_up_data = {
            "user": {
                "username": "Ken123",
                "email": "kenisme@andela.com",
                "password": "Pass@123"
            }
        }
        self.sign_up_data2 = {
            "user": {
                "username": "Ankodave",
                "email": "ankodave@andela.com",
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
        self.publish_data = {
            "is_published": True
        }
        self.article_data1 = {
            "title": "The weather",
            "description": "Its cold",
            "body": "Its really cold",
            "tagList": ["weather", "cold"]
        }
        self.article_data2 = {
            "title": "Reading",
            "description": "Books are cool",
            "body": "I like to read",
            "tagList": ["books", "novels"]
        }
        self.article_data3 = {
            "title": "Colours",
            "description": "Colours are  cool",
            "body": "Colors are interesting",
            "tagList": ["green", "black", "grey"]
        }
        self.article_data4 = {
            "title": "Shoes",
            "description": "Shoes are cool",
            "body": "Buying Shes",
            "tagList": ["Sneakers", "running Shoes"]
        }

    def register(self):
        """Sign up new user"""
        register = self.client.post(self.sign_up_url, self.sign_up_data,
                                    format='json')
        token = register.data['token']
        return token

    def register2(self):
        register = self.client.post(self.sign_up_url, self.sign_up_data2,
                                    format='json')
        token2 = register.data['token']
        return token2

    def test_filter_article_title(self):
        """Test that you can filter an article with a certain title."""

        token = self.register()
        # Create article
        self.client.post(self.article_listcreate_url, self.article_data1,
                         format='json',
                         HTTP_AUTHORIZATION='token {}'.format(token)
                         )
        self.client.post(self.article_listcreate_url, self.article_data,
                         format='json',
                         HTTP_AUTHORIZATION='token {}'.format(token)
                         )
        self.client.post(self.article_listcreate_url, self.article_data2,
                         format='json',
                         HTTP_AUTHORIZATION='token {}'.format(token)
                         )

        self.client.put(reverse('articles:publish_article',
                                kwargs={'slug': 'the-weather'}),
                        self.publish_data,
                        format='json',
                        HTTP_AUTHORIZATION='token {}'.format(token))
        self.client.put(reverse('articles:publish_article',
                                kwargs={'slug': 'coding-is-cool'}),
                        self.publish_data,
                        format='json',
                        HTTP_AUTHORIZATION='token {}'.format(token))
        self.client.put(reverse('articles:publish_article',
                                kwargs={'slug': 'shoes'}),
                        self.publish_data,
                        format='json',
                        HTTP_AUTHORIZATION='token {}'.format(token))
        all_articles = self.client.get(self.article_listcreate, format='json',
                                       HTTP_AUTHORIZATION='token {}'.format(
                                           token))
        response = self.client.get(self.filter_title_url,
                                   format='json',
                                   HTTP_AUTHORIZATION='token {}'.format(token))

        self.assertNotEqual(self.article_data1['title'],
                            all_articles.data['results'][0]['title'])
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn(self.article_data['title'],
                      response.data['results'][0]['title'])

    def test_filter_article_tag(self):
        """Test that you can filter an article with a specific tag"""

        token = self.register()
        # Create article
        self.client.post(self.article_listcreate_url, self.article_data,
                         format='json',
                         HTTP_AUTHORIZATION='token {}'.format(token)
                         )
        self.client.post(self.article_listcreate_url, self.article_data3,
                         format='json',
                         HTTP_AUTHORIZATION='token {}'.format(token)
                         )
        self.client.put(reverse('articles:publish_article',
                                kwargs={'slug': 'coding-is-cool'}),
                        self.publish_data,
                        format='json',
                        HTTP_AUTHORIZATION='token {}'.format(token))
        self.client.put(reverse('articles:publish_article',
                                kwargs={'slug': 'colours'}),
                        self.publish_data,
                        format='json',
                        HTTP_AUTHORIZATION='token {}'.format(token))
        all_articles = self.client.get(self.article_listcreate, format='json')
        response = self.client.get(self.filter_tag_url,
                                   format='json',
                                   HTTP_AUTHORIZATION='token {}'.format(token))
        self.assertNotEqual(self.article_data['tagList'],
                            all_articles.data['results'][0]['tagList'])
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertListEqual(self.article_data['tagList'],
                             response.data['results'][0]['tagList'])

    #
    def test_filter_author(self):
        """Test that you can filter an article with a specific tag"""

        token = self.register()
        token2 = self.register2()
        # Create article

        self.client.post(self.article_listcreate_url, self.article_data,
                         format='json',
                         HTTP_AUTHORIZATION='token {}'.format(token2)
                         )
        self.client.post(self.article_listcreate_url, self.article_data3,
                         format='json',
                         HTTP_AUTHORIZATION='token {}'.format(token)
                         )
        # publish articles
        self.client.put(reverse('articles:publish_article',
                                kwargs={'slug': 'coding-is-cool'}),
                        self.publish_data,
                        format='json',
                        HTTP_AUTHORIZATION='token {}'.format(token2))
        self.client.put(reverse('articles:publish_article',
                                kwargs={'slug': 'colours'}),
                        self.publish_data,
                        format='json',
                        HTTP_AUTHORIZATION='token {}'.format(token))
        all_articles = self.client.get(self.article_listcreate, format='json')
        response = self.client.get(self.filter_author_url,
                                   format='json',
                                   HTTP_AUTHORIZATION='token {}'.format(token))

        self.assertEqual(self.author_filter,
                         response.data['results'][0]['author'])
        self.assertNotEqual(self.author_filter2,
                            response.data['results'][0]['author'])
        self.assertEqual(response.status_code, status.HTTP_200_OK)


    def test_filter_all(self):
        """Test that you can filter an article with a specific title, taglist and author all at once """

        token = self.register()
        # Create article
        self.client.post(self.article_listcreate_url, self.article_data,
                         format='json',
                         HTTP_AUTHORIZATION='token {}'.format(token)
                         )
        self.client.post(self.article_listcreate_url, self.article_data4,
                         format='json',
                         HTTP_AUTHORIZATION='token {}'.format(token)
                         )
        self.client.post(self.article_listcreate_url, self.article_data2,
                         format='json',
                         HTTP_AUTHORIZATION='token {}'.format(token)
                         )
        # publish articles
        self.client.put(reverse('articles:publish_article',
                                kwargs={'slug': 'coding-is-cool'}),
                        self.publish_data,
                        format='json',
                        HTTP_AUTHORIZATION='token {}'.format(token))
        self.client.put(reverse('articles:publish_article',
                                kwargs={'slug': 'the-weather'}),
                        self.publish_data,
                        format='json',
                        HTTP_AUTHORIZATION='token {}'.format(token))
        self.client.put(reverse('articles:publish_article',
                                kwargs={'slug': 'colours'}),
                        self.publish_data,
                        format='json',
                        HTTP_AUTHORIZATION='token {}'.format(token))

        # get all articles
        all_articles = self.client.get(self.article_listcreate, format='json')
        response = self.client.get(self.filter_all,
                                   format='json',
                                   HTTP_AUTHORIZATION='token {}'.format(token))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertNotEqual(self.article_data['title'],
                            all_articles.data['results'][0])

        self.assertEqual(self.article_data['title'],
                         response.data['results'][0]['title'])
        self.assertListEqual(self.article_data['tagList'],
                             response.data['results'][0]['tagList'])
