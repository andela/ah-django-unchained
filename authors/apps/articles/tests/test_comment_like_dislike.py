from django.urls import reverse
from rest_framework.views import status
from rest_framework.test import APITestCase, APIClient


class CreateArticles(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.signup_url = reverse('authentication:auth-register')
        self.article_listcreate = reverse('articles:articles-listcreate')
        self.signup_data = {
            "user": {
                "username": "kennyg",
                "email": "ken@me.com",
                "password": "Kennyisme1!"
                }}
        self.create_article_data = {
            "title": "A new story",
            "body": "This is my story",
            "description": "Here is my story",
            "images": None,
            "tagList": ["dragons", "training"]
        }
        self.new_comment = {
            "body": "Good Work"
            }
        self.delete_item = {
            "is_deleted": True
        }
    
    def register(self):
        """Method to sign up user and get token"""
        register = self.client.post(self.signup_url,
                                    self.signup_data,
                                    format='json')

        token = register.data["token"]
        return token

    def create_comment(self, token):
        """Method to create a comment"""
        response = self.client.post(reverse('articles:create_comments',
                                    kwargs={'slug': 'a-new-story'}),
                                    self.new_comment,
                                    format='json',
                                    HTTP_AUTHORIZATION='token {}'.format(token)
                                    )
        return response
    
    def delete_comment(self, id, token):
        response = self.client.put(reverse('articles:delete_comments',
                                    kwargs={'slug': 'a-new-story', 'id': id}),
                                    self.delete_item,
                                    format='json',
                                    HTTP_AUTHORIZATION='token {}'.format(token)
                                    )
        return response

    def create_article(self, article, token):
        """Method to creates an article"""
        del article['images']
        response = self.client.post(self.article_listcreate,
                         article,
                         format='json',
                         HTTP_AUTHORIZATION='token {}'.format(token))
        return response
    
    def like_comment(self, id, token):
        """Method to like a comment"""
        response = self.client.put(reverse('articles:comment_like',
                                   kwargs={'slug': 'a-new-story', 'id': id}),
                                   self.new_comment,
                                   format='json',
                                   HTTP_AUTHORIZATION='token {}'.format(token))
        return response
    
    def dislike_comment(self, id, token):
        """Method to dislike a comment"""
        response = self.client.put(reverse('articles:comment_dislike',
                                   kwargs={'slug': 'a-new-story', 'id': id}),
                                   self.new_comment,
                                   format='json',
                                   HTTP_AUTHORIZATION='token {}'.format(token))
        return response

    def test_like_comment(self):
        """Test to like a comment"""
        token = self.register()
        self.create_article(self.create_article_data, token)
        response = self.create_comment(token)
        id = response.data['id']
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        response = self.like_comment(id, token)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data['user_id_likes'])
        self.assertFalse(response.data['user_id_dislikes'])
        self.assertEqual(response.data['likes_count'], 1)
        self.assertEqual(response.data['dislikes_count'], 0)
    
    def test_dislike_comment(self):
        """Test to dislike a comment"""
        token = self.register()
        self.create_article(self.create_article_data, token)
        response = self.create_comment(token)
        id = response.data['id']
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        response = self.dislike_comment(id, token)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(response.data['user_id_likes'])
        self.assertTrue(response.data['user_id_dislikes'])
        self.assertEqual(response.data['likes_count'], 0)
        self.assertEqual(response.data['dislikes_count'], 1)

    def test_unlike_comment(self):
        """Test to like a comment that has been liked"""
        token = self.register()
        self.create_article(self.create_article_data, token)
        response = self.create_comment(token)
        id = response.data['id']
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        response = self.like_comment(id, token)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data['user_id_likes'])
        self.assertFalse(response.data['user_id_dislikes'])
        response = self.like_comment(id, token)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(response.data['user_id_likes'])
        self.assertFalse(response.data['user_id_dislikes'])
        self.assertEqual(response.data['likes_count'], 0)
        self.assertEqual(response.data['dislikes_count'], 0)

    def test_to_dislike_a_disliked_comment(self):
        """Test to dislike a disliked comment"""
        token = self.register()
        self.create_article(self.create_article_data, token)
        response = self.create_comment(token)
        id = response.data['id']
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        response = self.dislike_comment(id, token)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(response.data['user_id_likes'])
        self.assertTrue(response.data['user_id_dislikes'])
        response = self.dislike_comment(id, token)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(response.data['user_id_likes'])
        self.assertFalse(response.data['user_id_dislikes'])
        self.assertEqual(response.data['likes_count'], 0)
        self.assertEqual(response.data['dislikes_count'], 0)
    
    def test_like_a_disliked_comment(self):
        """Test to like a disliked comment"""
        token = self.register()
        self.create_article(self.create_article_data, token)
        response = self.create_comment(token)
        id = response.data['id']
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        response = self.dislike_comment(id, token)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(response.data['user_id_likes'])
        self.assertTrue(response.data['user_id_dislikes'])
        response = self.like_comment(id, token)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data['user_id_likes'])
        self.assertFalse(response.data['user_id_dislikes'])
        self.assertEqual(response.data['likes_count'], 1)
        self.assertEqual(response.data['dislikes_count'], 0)

    def test_dislike_a_liked_comment(self):
        """Test to dislike a liked article"""
        token = self.register()
        self.create_article(self.create_article_data, token)
        response = self.create_comment(token)
        id = response.data['id']
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        response = self.like_comment(id, token)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data['user_id_likes'])
        self.assertFalse(response.data['user_id_dislikes'])
        response = self.dislike_comment(id, token)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(response.data['user_id_likes'])
        self.assertTrue(response.data['user_id_dislikes'])
        self.assertEqual(response.data['likes_count'], 0)
        self.assertEqual(response.data['dislikes_count'], 1)

    def test_like_a_deleted_comment(self):
        """Test to like a deleted comment"""
        token = self.register()
        self.create_article(self.create_article_data, token)
        response = self.create_comment(token)
        id = response.data['id']
        response = self.delete_comment(id, token)
        self.assertEqual(response.data['is_deleted'], True)
        response = self.like_comment(id, token)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data['detail'], 'A comment from this article does not exist')

    def test_unlike_a_deleted_comment(self):
        """Test to unlike a deleted comment"""
        token = self.register()
        self.create_article(self.create_article_data, token)
        response = self.create_comment(token)
        id = response.data['id']
        response = self.delete_comment(id, token)
        self.assertEqual(response.data['is_deleted'], True)
        response = self.dislike_comment(id, token)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data['detail'], 'A comment from this article does not exist')
    
    def test_like_comment_for_deleted_article(self):
        """Test to like a comment for a deleted article"""
        token = self.register()
        self.create_article(self.create_article_data, token)
        response = self.create_comment(token)
        id = response.data['id']
        response = self.client.put(reverse('articles:articles-delete',
                                           kwargs={'slug': 'a-new-story'}),
                                   self.delete_item,
                                   format='json',
                                   HTTP_AUTHORIZATION='token {}'.format(token))
        self.assertEqual(response.data['is_deleted'], True)
        response = self.like_comment(id, token)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data['detail'], 'Article does not exist')

    def test_dislike_comment_for_deleted_article(self):
        """Test to dislike a comment for a deleted article"""
        token = self.register()
        self.create_article(self.create_article_data, token)
        response = self.create_comment(token)
        id = response.data['id']
        response = self.client.put(reverse('articles:articles-delete',
                                           kwargs={'slug': 'a-new-story'}),
                                   self.delete_item,
                                   format='json',
                                   HTTP_AUTHORIZATION='token {}'.format(token))
        self.assertEqual(response.data['is_deleted'], True)
        response = self.dislike_comment(id, token)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data['detail'], 'Article does not exist')
