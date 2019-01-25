from django.urls import reverse
from rest_framework import status
from authors.apps.articles.tests.like_dislike_base_test import LikeDislike


class LikeDislikeTest(LikeDislike):
    """Test like or dislike articles."""
    def test_like_article(self):
        """Test like an article."""
        response = self.like_article()
        self.assertEqual(response.data['likes_count'], 1)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_dislike_article(self):
        """Test dislike an article."""
        response = self.dislike_article()
        self.assertEqual(response.data['dislikes_count'], 1)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_like_already_liked_article(self):
        """Test like already liked article."""
        slug = self.create_new_article()
        token = self.signup_user_one(self.user_signup_data2)
        self.client.put(
            reverse('articles:likes', kwargs={'slug': slug}),
            format='json',
            HTTP_AUTHORIZATION='token {}'.format(token))
        response = self.client.put(
            reverse('articles:likes', kwargs={'slug': slug}),
            format='json',
            HTTP_AUTHORIZATION='token {}'.format(token))
        self.assertEqual(response.data['likes_count'], 0)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_like_an_article_that_is_disliked(self):
        """Test like an article that has already been disliked."""
        slug = self.create_new_article()
        token = self.signup_user_one(self.user_signup_data2)
        self.client.put(
            reverse('articles:dislikes', kwargs={'slug': slug}),
            format='json',
            HTTP_AUTHORIZATION='token {}'.format(token))
        response = self.client.put(
            reverse('articles:likes', kwargs={'slug': slug}),
            format='json',
            HTTP_AUTHORIZATION='token {}'.format(token))
        self.assertEqual(response.data['likes_count'], 1)
        self.assertEqual(response.data['dislikes_count'], 0)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_dislike_article_already_liked(self):
        """Test dislike article that has already been liked."""
        slug = self.create_new_article()
        token = self.signup_user_one(self.user_signup_data2)
        self.client.put(
            reverse('articles:likes', kwargs={'slug': slug}),
            format='json',
            HTTP_AUTHORIZATION='token {}'.format(token))
        response = self.client.put(
            reverse('articles:dislikes', kwargs={'slug': slug}),
            format='json',
            HTTP_AUTHORIZATION='token {}'.format(token))

        self.assertEqual(response.data['likes_count'], 0)
        self.assertEqual(response.data['dislikes_count'], 1)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_dislike_article_already_disliked(self):
        """Test dislike article that has already been disliked."""
        slug = self.create_new_article()
        token = self.signup_user_one(self.user_signup_data2)
        self.client.put(
            reverse('articles:dislikes', kwargs={'slug': slug}),
            format='json',
            HTTP_AUTHORIZATION='token {}'.format(token))
        response = self.client.put(
            reverse('articles:dislikes', kwargs={'slug': slug}),
            format='json',
            HTTP_AUTHORIZATION='token {}'.format(token))
        self.assertEqual(response.data['likes_count'], 0)
        self.assertEqual(response.data['dislikes_count'], 0)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_rejects_like_unexisting_article(self):
        """Test rejects liking unexisting article."""
        slug = "myslug"
        token = self.signup_user_one(self.user_signup_data2)
        response = self.client.put(
            reverse('articles:likes', kwargs={'slug': slug}),
            format='json',
            HTTP_AUTHORIZATION='token {}'.format(token))
        self.assertEqual(response.data['detail'],
                         'An article with this slug does not exist')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

