import json
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from authors.apps.authentication.models import User


class BaseTestCase(TestCase):
    """Base tests to be used by all other tests"""
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

        self.article_details = {
            "title": "your first blog",
            "description": "this is your first blog",
            "body": "this is your first blog",
            "tagList": ["dragons", "training"],
        }

        self.follower = User.objects.create_user(
            username="andrew",
            email="andrew@gmail.com",
            password="this_user123@A")

        self.follower_data = {"user": {
            "email": "andrew@gmail.com",
            "password": "this_user123@A"
        }}

        login_res1 = self.client.post(
            self.login_url, self.follower_data, format='json')
        self.assertEqual(login_res1.status_code, status.HTTP_200_OK)
        self.token1 = login_res1.data["token"]


class NotificationsTestCase(BaseTestCase):
    def test_get_notification_on_article_creation(self):
        # follow user
        res = self.client.post(
            'http://127.0.0.1:8000/api/profiles/testuser/follow',
            HTTP_AUTHORIZATION='Token ' + self.token1)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

        # check notification is empty
        res2 = self.client.get(
            reverse("notifications:all-notifications"),
            HTTP_AUTHORIZATION='Token ' + self.token1)
        self.assertEqual(res2.status_code, status.HTTP_200_OK)
        self.assertEqual(res2.data["count"], 0)

        # followed user post article
        response = self.client.post(
            reverse("articles:articles-listcreate"),
            data=json.dumps(self.article_details),
            content_type="application/json",
            HTTP_AUTHORIZATION='Token ' + self.token)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # check notification is populated
        response2 = self.client.get(
            reverse("notifications:all-notifications"),
            HTTP_AUTHORIZATION='Token ' + self.token1)
        self.assertEqual(response2.status_code, status.HTTP_200_OK)
        self.assertEqual(response2.data["count"], 1)
