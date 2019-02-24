import json
from django.urls import reverse
from rest_framework.test import APIClient, APITestCase
from rest_framework import status
from authors.apps.authentication.models import User


class TestArticleRatings(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.login_url = reverse("authentication:auth-login")

        self.article_author = User.objects.create_user(
            username="testuser",
            email="testuser@gmail.com",
            password="this_user123@A")

        self.author_data = {"user": {
            "email": "testuser@gmail.com",
            "password": "this_user123@A"
        }}

        login_res = self.client.post(
            self.login_url, self.author_data, format='json')
        self.token = login_res.data["token"]

        article_details = {
            "title": "your first blog",
            "description": "this is your first blog",
            "body": "this is your first blog",
            "tagList": ["dragons", "training"],
        }

        self.response = self.client.post(
            reverse("articles:articles-listcreate"),
            data=json.dumps(article_details),
            content_type="application/json",
            HTTP_AUTHORIZATION='Token ' + self.token)

        self.slug = self.response.data['slug']

        self.rating_user = User.objects.create_user(
            username="andrew",
            email="andrew@gmail.com",
            password="this_user123@A")

        self.rating_user_data = {"user": {
            "email": "andrew@gmail.com",
            "password": "this_user123@A"
        }}

        login_res1 = self.client.post(
            self.login_url, self.rating_user_data, format='json')
        self.assertEqual(login_res1.status_code, status.HTTP_200_OK)
        self.token1 = login_res1.data["token"]

    def test_rate_article(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token1)
        slug = self.slug
        data = {"rate": 4}
        response = self.client.post(
            "/api/articles/{}/rate/".format(slug), data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(
            response.data['message'], 'Article successfully rated'
            )
        self.assertEqual(response.data['rating'], 4)

    def test_rate_with_number_outside_range(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        slug = self.slug
        data = {"rate": 6}
        response = self.client.post(
            "/api/articles/{}/rate/".format(slug), data=data,)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            'Give a rating between 1 to 5 inclusive', response.data['message'])

    def test_rate_non_existing_article(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        slug = "home-away"
        data = {"rate": 3}
        response = self.client.post(
            "/api/articles/{}/rate/".format(slug), data=data)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertIn('Article not found', response.data['detail'])

    def test_rating_by_unauthenticated_user(self):
        slug = self.slug
        data = {"rate": 4}
        response = self.client.post(
            "/api/articles/{}/rate/".format(slug), data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_rate_own_article(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        slug = self.slug
        data = {"rate": 4}
        response = self.client.post(
            "/api/articles/{}/rate/".format(slug), data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.data["error"],
            "You are not allowed to rate your own article"
            )

    def test_update_ratings(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token1)

        # assert that the first rating is made successfully
        slug = self.slug
        data1 = {"rate": 4}
        res1 = self.client.post(
            "/api/articles/{}/rate/".format(slug), data=data1, format='json')
        self.assertEqual(res1.status_code, status.HTTP_201_CREATED)

        # assert that the rating is 4
        res2 = self.client.put(
            "/api/articles/rate/{}/".format(slug))
        self.assertEqual(res2.status_code, status.HTTP_200_OK)
        self.assertEqual(res2.data['ratings'], 4)

        # assert that rating can be modified
        data2 = {"rate": 3}
        res3 = self.client.post(
            "/api/articles/{}/rate/".format(slug), data=data2, format='json')
        self.assertEqual(res3.status_code, status.HTTP_201_CREATED)

        # assert that the new rating is 3
        res4 = self.client.put(
            "/api/articles/rate/{}/".format(slug))
        self.assertEqual(res4.status_code, status.HTTP_200_OK)
        self.assertEqual(res4.data['ratings'], 3)

    def test_view_article_rating(self):
        # assert that ratings of an article that's not rated is 0
        slug = self.slug
        res1 = self.client.put(
            "/api/articles/rate/{}/".format(slug))
        self.assertEqual(res1.status_code, status.HTTP_200_OK)
        self.assertEqual(res1.data['ratings'], 0)

        # assert that the article is rated
        data = {"rate": 4}
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token1)
        res2 = self.client.post(
            "/api/articles/{}/rate/".format(slug), data=data, format='json')
        self.assertEqual(res2.status_code, status.HTTP_201_CREATED)

        # assert that the new rating is 4
        res3 = self.client.put(
            "/api/articles/rate/{}/".format(slug))
        self.assertEqual(res3.status_code, status.HTTP_200_OK)
        self.assertEqual(res3.data['ratings'], 4)
