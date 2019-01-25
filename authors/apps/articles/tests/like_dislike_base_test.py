from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from authors.apps.articles.models import Article


class LikeDislike(APITestCase):
    """Base test case for like or dislike articles."""
    def setUp(self):
        self.client = APIClient()
        self.signup_url = reverse('authentication:auth-register')
        self.create_article_url = reverse('articles:articles-listcreate')
        self.user_signup_data = {
            "user": {
                "username": "AndelaKenya",
                "email": "andela@andela.com",
                "password": "Password@123"
                }}
        self.user_signup_data2 = {
            "user": {
                "username": "Andela123",
                "email": "andela123@gmail.com",
                "password": "Password@123"
                }}
        self.create_article_data = {
            "title": "A new story",
            "body": "This is my story",
            "description": "Here is my story"
        }

    def signup_user_one(self, user_details):
        """Register a new user."""
        response = self.client.post(self.signup_url,
                                    user_details,
                                    format='json')
        token = response.data['token']
        return token

    def create_new_article(self):
        """Create an article."""
        token = self.signup_user_one(self.user_signup_data)
        response = self.client.post(
            self.create_article_url,
            self.create_article_data,
            format='json',
            HTTP_AUTHORIZATION='token {}'.format(token))
        slug = response.data['slug']
        return slug

    def like_article(self):
        """Method for liking an article."""
        slug = self.create_new_article()
        token = self.signup_user_one(self.user_signup_data2)
        result = self.client.put(
            reverse('articles:likes', kwargs={'slug': slug}),
            format='json',
            HTTP_AUTHORIZATION='token {}'.format(token))
        return result

    def dislike_article(self):
        """Method for disliking an article."""
        slug = self.create_new_article()
        token = self.signup_user_one(self.user_signup_data2)
        result = self.client.put(
            reverse('articles:dislikes', kwargs={'slug': slug}),
            format='json',
            HTTP_AUTHORIZATION='token {}'.format(token))
        return result
