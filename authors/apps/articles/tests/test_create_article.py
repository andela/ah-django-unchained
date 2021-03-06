import json
from django.urls import reverse
from rest_framework.views import status
from rest_framework.test import APITestCase, APIClient
from .stories import small_story, medium_story, huge_story


class CreateArticles(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.login_url = reverse('authentication:auth-login')
        self.signup_url = reverse('authentication:auth-register')
        self.article_listcreate = reverse('articles:articles-listcreate')
        self.article_favorite = reverse('articles:articles-favorite',
                                        kwargs={'slug': 'my-story'})
        self.publish_data = {
            "is_published": True
        }
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
            "title": "my story",
            "is_published": False,
            "body": "This is my story",
            "description": "Here is my story",
            "images": None,
            "tagList": ["dragons", "training"]
        }
        self.create_article_data2 = {
            "title": "The beginning",
            "body": "This begins now",
            "is_published": False,
            "description": "Here is my story",
            "images": None,
            "tagList": ["dragons", "training"]
        }
        self.delete_article = {
            "is_deleted": True
        }

        self.small_body = {
            "title": "small",
            "body": small_story,
            "description": "Here is my story",
            "images": None,
            "tagList": ["dragons", "training"]
        }

        self.medium_body = {
            "title": "medium",
            "body": medium_story,
            "description": "Here is my story",
            "images": None,
            "tagList": ["dragons", "training"]
        }

        self.huge_body = {
            "title": "huge",
            "body": huge_story,
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

    def signup_user_two(self):
        """Function to register user two and return their token"""
        register = self.client.post(self.signup_url,
                                    self.signup_data2,
                                    format='json')
        token = register.data['token']
        return token

    def create_article(self, article, token):
        del article['images']
        response = self.client.post(self.article_listcreate,
                                    article,
                                    format='json',
                                    HTTP_AUTHORIZATION='token {}'.format(
                                        token))
        return response

    def post_article_articles(self, data):
        token = self.signup_user_one()
        del data['images']
        response = self.client.post(
            self.article_listcreate,
            data,
            format='json',
            HTTP_AUTHORIZATION='token {}'.format(token))
        return response

    def test_fetch_all_published_articles(self):
        """Tests to fetch all articles"""
        token = self.signup_user_one()
        # create article
        self.create_article(self.create_article_data, token)
        self.create_article(self.create_article_data2, token)
        # publish articles
        self.assertNotEqual(self.create_article_data['is_published'], True)
        self.client.put(reverse('articles:publish_article',
                                kwargs={'slug': 'my-story'}),
                        self.publish_data,
                        format='json',
                        HTTP_AUTHORIZATION='token {}'.format(token))
        self.client.put(reverse('articles:publish_article',
                                kwargs={'slug': 'the-beginning'}),
                        self.publish_data,
                        format='json',
                        HTTP_AUTHORIZATION='token {}'.format(token))
        response = self.client.get(self.article_listcreate, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data['results'][0]['is_published'],True)
        self.assertIn('count', response.data)
        self.assertIn('next', response.data)
        self.assertIn('previous', response.data)

        self.assertEqual(self.create_article_data['title'],
                         response.data['results'][1]['title'])
        self.assertEqual(self.create_article_data['body'],
                         response.data['results'][1]['body'])
        self.assertEqual(self.create_article_data2['body'],
                         response.data['results'][0]['body'])
        self.assertEqual(self.create_article_data['description'],
                         response.data['results'][1]['description'])
        self.assertEqual(self.create_article_data2['description'],
                         response.data['results'][0]['description'])
        self.assertIn(self.create_article_data2['tagList'][0],
                      response.data['results'][0]['tagList'])

    def test_create_article_draft(self):
        """Test to create article draft"""
        token = self.signup_user_one()
        del self.create_article_data['images']
        response = self.client.post(self.article_listcreate,
                                    self.create_article_data,
                                    format='json',
                                    HTTP_AUTHORIZATION='token {}'.format(
                                        token))
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertFalse(response.data['is_published'], False)
        self.assertEqual(self.create_article_data['title'],
                         response.data['title'])
        self.assertEqual(self.create_article_data['body'],
                         response.data['body'])
        self.assertEqual(self.create_article_data['description'],
                         response.data['description'])
        self.assertIn(self.create_article_data2['tagList'][0],
                      response.data['tagList'])

    def test_get_all_article_drafts(self):
        token = self.signup_user_one()
        self.create_article(self.create_article_data, token)
        self.create_article(self.create_article_data2, token)
        response = self.client.get(reverse('articles:get_all_drafts'),
                                   format='json',
                                   HTTP_AUTHORIZATION='token {}'.format(token))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn(self.create_article_data2['title'],
                      response.data['results'][0]['title'])

    def test_get_single_published_article(self):
        """Test to get a single article"""
        token = self.signup_user_one()
        self.create_article(self.create_article_data, token)
        self.client.put(reverse('articles:publish_article',
                                kwargs={'slug': 'my-story'}),
                        self.publish_data,
                        format='json',
                        HTTP_AUTHORIZATION='token {}'.format(token))
        response = self.client.get(reverse('articles:articles-retrieveupdate',
                                           kwargs={'slug': 'my-story'}),
                                   format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.create_article_data['title'],
                         response.data['title'])
        self.assertEqual(self.create_article_data['body'],
                         response.data['body'])
        self.assertEqual(self.create_article_data['description'],
                         response.data['description'])
        self.assertIn(self.create_article_data2['tagList'][0],
                      response.data['tagList'])

    def test_unauthorized_article_update(self):
        """Test to update an article created by another user"""
        token = self.signup_user_one()
        self.create_article(self.create_article_data, token)
        self.client.put(reverse('articles:publish_article',
                                kwargs={'slug': 'my-story'}),
                        self.publish_data,
                        format='json',
                        HTTP_AUTHORIZATION='token {}'.format(token))
        token2 = self.signup_user_two()
        response = self.client.put(reverse('articles:articles-retrieveupdate',
                                           kwargs={'slug': 'my-story'}),
                                   self.create_article_data2,
                                   format='json',
                                   HTTP_AUTHORIZATION='token {}'.format(
                                       token2))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_authorized_article_update(self):
        """Test to legitimately update an article created by a user"""
        token = self.signup_user_one()
        self.create_article(self.create_article_data, token)
        self.client.put(reverse('articles:publish_article',
                                kwargs={'slug': 'my-story'}),
                        self.publish_data,
                        format='json',
                        HTTP_AUTHORIZATION='token {}'.format(token))
        del self.create_article_data2['images']
        response = self.client.put(reverse('articles:articles-retrieveupdate',
                                           kwargs={'slug': 'my-story'}),
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
        self.create_article(self.create_article_data, token)
        self.client.put(reverse('articles:publish_article',
                                kwargs={'slug': 'my-story'}),
                        self.publish_data,
                        format='json',
                        HTTP_AUTHORIZATION='token {}'.format(token))
        response = self.client.put(reverse('articles:articles-delete',
                                           kwargs={'slug': 'my-story'}),
                                   self.delete_article,
                                   format='json',
                                   HTTP_AUTHORIZATION='token {}'.format(token))
        self.assertEqual(self.delete_article['is_deleted'],
                         response.data['is_deleted'])
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_unauthorized_delete_article(self):
        """Test to delete someone else's article"""
        token = self.signup_user_one()
        self.create_article(self.create_article_data, token)
        self.client.put(reverse('articles:publish_article',
                                kwargs={'slug': 'my-story'}),
                        self.publish_data,
                        format='json',
                        HTTP_AUTHORIZATION='token {}'.format(token))
        token2 = self.signup_user_two()
        response = self.client.put(reverse('articles:articles-delete',
                                           kwargs={'slug': 'my-story'}),
                                   self.delete_article,
                                   format='json',
                                   HTTP_AUTHORIZATION='token {}'.format(
                                       token2))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual('You are not allowed to edit or delete this object',
                         response.data['detail'])

    def test_to_fetch_non_exisiting_article(self):
        """Test to fetch an article that does not exist"""
        response = self.client.get(reverse('articles:articles-retrieveupdate',
                                           kwargs={'slug': 'a-new-story'}),
                                   format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual('Not found.', response.data['detail'])

    def test_favorite_article(self):
        """Test to favorite an article"""
        token = self.signup_user_one()
        self.create_article(self.create_article_data, token)
        response = self.client.post(self.article_favorite,
                                    format='json',
                                    HTTP_AUTHORIZATION='token {}'.format(
                                        token))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['favorite'], True)

    def test_unfavorite_a_favorited_article(self):
        """Test to unfavorite an article that had previously been favorited"""
        token = self.signup_user_one()
        self.create_article(self.create_article_data, token)
        response = self.client.post(self.article_favorite,
                                    format='json',
                                    HTTP_AUTHORIZATION='token {}'.format(
                                        token))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['favorite'], True)
        response = self.client.delete(self.article_favorite,
                                      format='json',
                                      HTTP_AUTHORIZATION='token {}'.format(
                                          token))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['favorite'], False)

    def test_to_favorite_a_favorited_article(self):
        """Test to favorite a favorited article"""
        token = self.signup_user_one()
        self.create_article(self.create_article_data, token)
        response = self.client.post(self.article_favorite,
                                    format='json',
                                    HTTP_AUTHORIZATION='token {}'.format(
                                        token))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['favorite'], True)
        response = self.client.post(self.article_favorite,
                                    format='json',
                                    HTTP_AUTHORIZATION='token {}'.format(
                                        token))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'],
                         'Article already favorited.')

    def test_to_unfavorite_a_unfavorited_article(self):
        """Test to unfavorite an unfavorited article"""
        token = self.signup_user_one()
        self.create_article(self.create_article_data, token)
        self.client.post(self.article_favorite,
                         format='json',
                         HTTP_AUTHORIZATION='token {}'.format(token))
        response = self.client.delete(self.article_favorite,
                                      format='json',
                                      HTTP_AUTHORIZATION='token {}'.format(
                                          token))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['favorite'], False)
        response = self.client.delete(self.article_favorite,
                                      format='json',
                                      HTTP_AUTHORIZATION='token {}'.format(
                                          token))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'],
                         'Article already unfavorited.')

    def test_read_time_small_article(self):
        """Tests the read time for a small article"""
        self.post_article_articles(self.small_body)
        read_url = reverse('articles:articles-read', kwargs={'slug': 'small'})
        response = self.client.get(read_url, format='json')
        data = {'read_time': 0}
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(json.loads(response.content), data)

    def test_read_time_medium_article(self):
        """Tests the read time for a medium article"""
        self.post_article_articles(self.medium_body)
        read_url = reverse('articles:articles-read', kwargs={'slug': 'medium'})
        response = self.client.get(read_url, format='json')
        data = {'read_time': 3}
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(json.loads(response.content), data)

    def test_read_time_huge_article(self):
        """Tests the read time for a huge article"""
        self.post_article_articles(self.huge_body)
        read_url = reverse('articles:articles-read', kwargs={'slug': 'huge'})
        response = self.client.get(read_url, format='json')
        data = {'read_time': 7}
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(json.loads(response.content), data)
