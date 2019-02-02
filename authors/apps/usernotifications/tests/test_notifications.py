import json
from django.test import TestCase
from django.urls import reverse
from django.core import mail
from django.conf import settings
from rest_framework.test import APIClient
from rest_framework import status
from authors.apps.authentication.models import User


class BaseTestCase(TestCase):
    """
    Base tests to be used by all other tests
    """
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

        self.follower2 = User.objects.create_user(
            username="maggy66",
            email="maggy@gmail.com",
            password="this_user123@A")

        self.follower2_data = {"user": {
            "email": "maggy@gmail.com",
            "password": "this_user123@A"
        }}

        login_res2 = self.client.post(
            self.login_url, self.follower2_data, format='json')
        self.assertEqual(login_res2.status_code, status.HTTP_200_OK)
        self.token2 = login_res2.data["token"]


class NotificationsTestCase(BaseTestCase):
    """
    class for notification tests
    """
    def test_get_notification_on_article_creation(self):
        """
        test user will get notification
        when users they follow post articles
        """
        # two users follow a particular user
        response1 = self.client.post(
            'http://127.0.0.1:8000/api/profiles/testuser/follow',
            HTTP_AUTHORIZATION='Token ' + self.token1)
        self.assertEqual(response1.status_code, status.HTTP_200_OK)

        response2 = self.client.post(
            'http://127.0.0.1:8000/api/profiles/testuser/follow',
            HTTP_AUTHORIZATION='Token ' + self.token2)
        self.assertEqual(response2.status_code, status.HTTP_200_OK)

        # unsubscribe one user
        response3 = self.client.put(
            'http://127.0.0.1:8000/api/notifications/unsubscribe/',
            HTTP_AUTHORIZATION='Token ' + self.token2)
        self.assertEqual(response3.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response3.data['message'],
            "You have successfully unsubscribed from app notifications")
        self.assertTrue(response3.data["email"])
        self.assertFalse(response3.data["app"])

        # check notification is empty
        response4 = self.client.get(
            reverse("notifications:all-notifications"),
            HTTP_AUTHORIZATION='Token ' + self.token1)
        self.assertEqual(response4.status_code, status.HTTP_200_OK)
        self.assertEqual(response4.data["count"], 0)

        # followed user post article
        response5 = self.client.post(
            reverse("articles:articles-listcreate"),
            data=json.dumps(self.article_details),
            content_type="application/json",
            HTTP_AUTHORIZATION='Token ' + self.token)
        self.assertEqual(response5.status_code, status.HTTP_201_CREATED)

        # check notification is populated
        response6 = self.client.get(
            reverse("notifications:all-notifications"),
            HTTP_AUTHORIZATION='Token ' + self.token1)
        self.assertEqual(response6.status_code, status.HTTP_200_OK)
        self.assertEqual(response6.data["count"], 1)
        self.assertIn(
            'testuser posted an article on',
            response6.data["notifications"][0]["description"]
            )

        # check notification is not populated for the unsubscribed user
        response7 = self.client.get(
            reverse("notifications:all-notifications"),
            HTTP_AUTHORIZATION='Token ' + self.token2)
        self.assertEqual(response7.status_code, status.HTTP_200_OK)
        self.assertEqual(response7.data["count"], 0)

    def test_get_notification_when_followed(self):
        """
        test user will get notification when followed
        """
        # assert no notifcations
        response1 = self.client.get(
            reverse("notifications:all-notifications"),
            HTTP_AUTHORIZATION='Token ' + self.token)
        self.assertEqual(response1.status_code, status.HTTP_200_OK)
        self.assertEqual(response1.data["count"], 0)

        # send follow request
        response2 = self.client.post(
            'http://127.0.0.1:8000/api/profiles/testuser/follow',
            HTTP_AUTHORIZATION='Token ' + self.token1)
        self.assertEqual(response2.status_code, status.HTTP_200_OK)

        # assert notifcation is available
        response3 = self.client.get(
            reverse("notifications:all-notifications"),
            HTTP_AUTHORIZATION='Token ' + self.token)
        self.assertEqual(response3.status_code, status.HTTP_200_OK)
        self.assertEqual(response3.data["count"], 1)
        self.assertIn(
            'andrew followed you on',
            response3.data["notifications"][0]["description"]
            )

    def test_send_email_notification(self):
        """
        test that email notification is sent
        """
        # empty the test outbox
        mail.outbox = []
        self.assertEqual(len(mail.outbox), 0)
        mail.send_mail(
            'Authors Haven Notifications', 'Here is the message.',
            settings.EMAIL_HOST_USER, ['andrewhinga5@gmail.com'],
            fail_silently=False,
        )
        # test that one message has been sent.
        self.assertEqual(len(mail.outbox), 1)
        # verify that the subject of the first message is correct.
        self.assertEqual(mail.outbox[0].subject,
                         'Authors Haven Notifications')

    def test_unauthenticated_user_cannot_view_notifications(self):
        """
        test an authenticated user won't view notifications
        """
        response = self.client.get(reverse("notifications:all-notifications"))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class SubscribeUnsubscribeTestCase(BaseTestCase):
    """
    test class for subscribing and unsubscribing to notifications
    """
    def test_unsubscribe_from_in_app(self):
        """
        test user can unsubscribe from notifications
        test user can subscribe back to notifications
        """
        # test unsubscribe
        response1 = self.client.put(
            'http://127.0.0.1:8000/api/notifications/unsubscribe/',
            HTTP_AUTHORIZATION='Token ' + self.token1)
        self.assertEqual(response1.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response1.data['message'],
            "You have successfully unsubscribed from app notifications")
        self.assertTrue(response1.data["email"])
        self.assertFalse(response1.data["app"])

        # test unsubscribed user won't receive notifications
        # follow user
        response2 = self.client.post(
            'http://127.0.0.1:8000/api/profiles/testuser/follow',
            HTTP_AUTHORIZATION='Token ' + self.token1)
        self.assertEqual(response2.status_code, status.HTTP_200_OK)

        # check notification is empty
        response3 = self.client.get(
            reverse("notifications:all-notifications"),
            HTTP_AUTHORIZATION='Token ' + self.token1)
        self.assertEqual(response3.status_code, status.HTTP_200_OK)
        self.assertEqual(response3.data["count"], 0)

        # followed user post article
        response4 = self.client.post(
            reverse("articles:articles-listcreate"),
            data=json.dumps(self.article_details),
            content_type="application/json",
            HTTP_AUTHORIZATION='Token ' + self.token)
        self.assertEqual(response4.status_code, status.HTTP_201_CREATED)

        # check notification is still empty
        response5 = self.client.get(
            reverse("notifications:all-notifications"),
            HTTP_AUTHORIZATION='Token ' + self.token1)
        self.assertEqual(response5.status_code, status.HTTP_200_OK)
        self.assertEqual(response5.data["count"], 0)

        # test user can subscribe back
        response6 = self.client.post(
            'http://127.0.0.1:8000/api/notifications/subscribe/',
            HTTP_AUTHORIZATION='Token ' + self.token1)
        self.assertEqual(response6.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response6.data['message'],
            "You have successfully subscribed to notifications")
        self.assertTrue(response6.data["email"])
        self.assertTrue(response6.data["app"])

    def test_unauthenticated_unsubscribe(self):
        """
        test an unauthenticated user cannot subscribe
        to notifications
        """
        response1 = self.client.put(
            'http://127.0.0.1:8000/api/notifications/subscribe/')
        self.assertEqual(response1.status_code, status.HTTP_403_FORBIDDEN)

    def test_unsubscribe_from_email_notifications(self):
        """
        test that user can unsubscribe from email notifications
        """
        unsubscribe_url = reverse('notifications:email-unsubscribe',
                             kwargs={"token": self.token})
        response = self.client.get(
            unsubscribe_url, HTTP_AUTHORIZATION='Token ' + self.token)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
