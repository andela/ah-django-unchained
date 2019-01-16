from rest_framework import status
from .base_test import BaseTestCase


class TestUserFollow(BaseTestCase):
    """Test the follow/unfollow functionality"""
    friend_url = 'http://127.0.0.1:8000/api/profiles'

    def test_follow_other_user(self):
        self.client.post(
            'http://127.0.0.1:8000/api/users/',
            data=self.new_user
            )
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        response = self.client.post(self.friend_url + '/andrew/follow')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        assert response.data['username'] == 'andrew'

    def test_unfollow_other_user(self):
        self.client.post(
            'http://127.0.0.1:8000/api/users/',
            data=self.new_user
            )
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        res1 = self.client.post(self.friend_url + '/andrew/follow')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        assert response.data['username'] == 'andrew'
        res2 = self.client.delete((self.friend_url, '/andrew/unfollow'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        assert res2.data['username'] == 'andrew'

    def test_follow_self(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        respsonse = self.client.post(self.friend_url + '/testuser/follow')
        self.assertEqual(respsonse.status_code, status.HTTP_406_NOT_ACCEPTABLE)
        assert response.data['message'] == 'You cannot follow yourself'

    def test_follow_nonexisting_user(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        response = self.client.post(self.friend_url, '/andrew12/follow')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        assert response.data['detail'] == 'Not found.'

    def test_get_followers(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        response = self.client.get(self.friend_url + '/andrew/followers')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        assert response.data["count"] == 0

    def test_get_following(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        response = self.client.get(self.friend_url + '/andrew/following')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        assert response.data["count"] == 0
