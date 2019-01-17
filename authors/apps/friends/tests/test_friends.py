from rest_framework import status
from .base_tests import BaseTestCase
from authors.apps.authentication.models import User


class TestUserFollow(BaseTestCase):
    """Test the follow/unfollow functionality"""
    friend_url = 'http://127.0.0.1:8000/api/users'

    def test_follow_other_user(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        response = self.client.post(self.friend_url + '/andrew/follow')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['email'], 'andrewhinga5@gmail.com')
        self.assertEqual(response.data['username'], 'andrew')

    def test_only_authenticated_users_can_follow(self):
        response = self.client.post(self.friend_url + '/andrew/follow')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_unfollow_other_user(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        res1 = self.client.post(self.friend_url + '/andrew/follow')
        self.assertEqual(res1.status_code, status.HTTP_200_OK)
        assert res1.data['username'] == 'andrew'
        res2 = self.client.delete(self.friend_url + '/andrew/unfollow')
        self.assertEqual(res2.status_code, status.HTTP_200_OK)
        self.assertEqual(res2.data['username'], 'andrew')

    def test_follow_self(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        response = self.client.post(self.friend_url + '/testuser/follow')
        self.assertEqual(response.status_code, status.HTTP_406_NOT_ACCEPTABLE)
        self.assertEqual(
            response.data['message'], 'You cannot follow yourself')

    def test_unfollow_self(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        response = self.client.delete(self.friend_url + '/testuser/unfollow')
        self.assertEqual(response.status_code, status.HTTP_406_NOT_ACCEPTABLE)
        self.assertEqual(
            response.data['message'], 'You cannot unfollow yourself')

    def test_follow_nonexisting_user(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        response = self.client.post(self.friend_url + '/ken/follow')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        assert response.data['detail'] == 'Not found.'

    def test_unfollow_nonexisting_user(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        response = self.client.delete(self.friend_url + '/ken/unfollow')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        assert response.data['detail'] == 'Not found.'

    def test_get_followers(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        response = self.client.get(self.friend_url + '/andrew/followers')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)

    def test_get_following(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        response = self.client.get(self.friend_url + '/andrew/following')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)
