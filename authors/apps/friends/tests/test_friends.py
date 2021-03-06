from rest_framework import status
from .base_tests import BaseTestCase
from authors.apps.authentication.models import User


class TestUserFollow(BaseTestCase):
    """Test the follow/unfollow functionality"""
    friend_url = 'http://127.0.0.1:8000/api/profiles'

    def test_follow_other_user(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        response = self.client.post(self.friend_url + '/andrew/follow')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["number_of_followers"], 1)

    def test_only_authenticated_users_can_follow(self):
        response = self.client.post(self.friend_url + '/andrew/follow')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_unfollow_other_user(self):
        # test that a user is followed successfully
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        res1 = self.client.post(self.friend_url + '/andrew/follow')
        self.assertEqual(res1.status_code, status.HTTP_200_OK)
        self.assertEqual(res1.data["number_of_followers"], 1)
        # test that a user is unfollowed successfullly
        res2 = self.client.delete(self.friend_url + '/andrew/follow')
        self.assertEqual(res2.status_code, status.HTTP_200_OK)
        self.assertEqual(res2.data["number_of_followers"], 0)

    def test_follow_self(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        response = self.client.post(self.friend_url + '/testuser/follow')
        self.assertEqual(response.status_code, status.HTTP_406_NOT_ACCEPTABLE)
        self.assertEqual(
            response.data['message'], 'You cannot follow yourself')

    def test_unfollow_self(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        response = self.client.delete(self.friend_url + '/testuser/follow')
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
        response = self.client.delete(self.friend_url + '/ken/follow')
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

    def test_follow_user_that_i_follow(self):
        # first test to follow a user
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        response = self.client.post(self.friend_url + '/andrew/follow')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["number_of_followers"], 1)
        # second test to follow the same user
        res2 = self.client.post(self.friend_url + '/andrew/follow')
        self.assertEqual(res2.status_code, status.HTTP_406_NOT_ACCEPTABLE)
        self.assertEqual(
            res2.data['message'], 'you already follow this user')

    def test_unfollow_user_i_dont_follow(self):
        # first test that a user is followed successfully
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        res1 = self.client.post(self.friend_url + '/andrew/follow')
        self.assertEqual(res1.status_code, status.HTTP_200_OK)
        self.assertEqual(res1.data["number_of_followers"], 1)
        # second test that a user is unfollowed successfullly
        res2 = self.client.delete(self.friend_url + '/andrew/follow')
        self.assertEqual(res2.status_code, status.HTTP_200_OK)
        self.assertEqual(res2.data["number_of_followers"], 0)
        # third test that i cannot unfollow a user i don't follow
        res3 = self.client.delete(self.friend_url + '/andrew/follow')
        self.assertEqual(res3.status_code, status.HTTP_406_NOT_ACCEPTABLE)
        self.assertEqual(res3.data['message'], "you don't follow this user")
