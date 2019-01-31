import json
from django.urls import reverse
from rest_framework.views import status
from rest_framework.test import APITestCase, APIClient


class TestBookmarks(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.signup_url = reverse('authentication:auth-register')
        self.article_url = reverse('articles:articles-listcreate')
        self.post_bookmark_url = reverse(
            'bookmarks:create-bookmark',
            kwargs={'slug': 'tdd'})
        self.get_bookmark_url = reverse('bookmarks:bookmarks')
        self.delete_bookmark_url = reverse(
            'bookmarks:delete-bookmark',
            kwargs={'slug': 'tdd'})
        self.signup_data = {
            "user": {
                "username": "johndoe",
                "email": "johndoe@gmail.com",
                "password": "Kennyisme1!"
            }}
        self.create_article_data = {
            "title": "TDD",
            "body": "This is my story",
            "description": "Here is my story",
            "tagList": ["dragons", "training"]
        }

    def signup_user(self):
        """Function to register user one and return their token"""
        register = self.client.post(self.signup_url,
                                    self.signup_data,
                                    format='json')
        token = json.loads(register.content)['user']['token']
        return token

    def create_article(self, article, token):
        response = self.client.post(
            self.article_url,
            article,
            format='json',
            HTTP_AUTHORIZATION='token {}'.format(token))
        return response

    def test_bookmark_invalid_article(self):
        """Test getting an invalid article"""
        token = self.signup_user()
        response = self.client.post(
            self.post_bookmark_url,
            format='json',
            HTTP_AUTHORIZATION='token {}'.format(token))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(
            json.loads(response.content),
            {'error': 'Article tdd does not exist'})

    def test_bookmarking_an_article(self):
        """Test bookmarking an article"""
        token = self.signup_user()
        self.create_article(self.create_article_data, token)
        response = self.client.post(
            self.post_bookmark_url,
            format='json',
            HTTP_AUTHORIZATION='token {}'.format(token))
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(
            json.loads(response.content),
            {'message': 'Article  has been added to your bookmark'})

    def test_get_all_bookmarks(self):
        """Test getting all bookmarks"""
        token = self.signup_user()
        self.create_article(self.create_article_data, token)
        self.client.post(
            self.post_bookmark_url,
            format='json',
            HTTP_AUTHORIZATION='token {}'.format(token))

        response = self.client.get(
            self.get_bookmark_url,
            format='json',
            HTTP_AUTHORIZATION='token {}'.format(token)
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('my_bookmarks', json.loads(response.content))

    def test_get_no_bookmarks(self):
        """Test getting zero  bookmarks """
        token = self.signup_user()
        self.create_article(self.create_article_data, token)
        response = self.client.get(
            self.get_bookmark_url,
            format='json',
            HTTP_AUTHORIZATION='token {}'.format(token)
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(
            json.loads(response.content),
            {'error': 'You have no bookmark available'})

    def test_delete_bookmarks(self):
        """test deleting bookmarks"""
        token = self.signup_user()
        self.create_article(self.create_article_data, token)
        self.client.post(
            self.post_bookmark_url,
            format='json',
            HTTP_AUTHORIZATION='token {}'.format(token))

        response = self.client.delete(
            self.delete_bookmark_url,
            format='json',
            HTTP_AUTHORIZATION='token {}'.format(token)
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            json.loads(response.content),
            {'message': 'Article has been remove from your bookmark'})

    def test_delete_none_existing_bookmarks(self):
        """Test deleting bookmarks that does not exist"""
        token = self.signup_user()
        self.create_article(self.create_article_data, token)
        response = self.client.delete(
            self.delete_bookmark_url,
            format='json',
            HTTP_AUTHORIZATION='token {}'.format(token)
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(
            json.loads(response.content),
            {'error': 'Article does not exist in your bookmark'})

    def test_posting_with_logged_in_user(self):
        """Test bookmarking an article when not logged in"""
        token = self.signup_user()
        self.create_article(self.create_article_data, token)
        response = self.client.post(
            self.post_bookmark_url,
            format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(
            json.loads(response.content),
            {'detail': 'Authentication credentials were not provided.'})
