import json
from django.urls import reverse
from rest_framework.views import status
from rest_framework.test import APITestCase, APIClient


class CommentsTestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.signup_url = reverse('authentication:auth-register')
        self.create_article_url = reverse('articles:articles-listcreate')
        self.user_two_details = {
            "user": {
                "username": "andela",
                "email": "andela@andela.com",
                "password": "Password@123"
                }}

        self.create_article_data = {
            "title": "Programming Languages",
            "body": "There are variety of programming languagr",
            "description": "Programming",
            "tagList": ["Programming", "language", "python"]
            }
        self.highlighted_text = {
            "comment": {
                "body": "Good work here!!",
                "start_highlight_position": 2,
                "end_highlight_position": 15
                }}
        self.selection_start_index_larger_than_end_index = {
            "comment": {
                "body": "Good work here!!",
                "start_highlight_position": 28,
                "end_highlight_position": 15
                }}
        self.invalid_index_datatype = {
            "comment": {
                "body": "Good work here!!",
                "start_highlight_position": "one",
                "end_highlight_position": 15
                }}
        self.missing_field = {
            "comment": {
                "body": "Good work here!!",
                "end_highlight_position": 15
                }}

        self.update_comment = {
            "comment": {
                "body": "Nice Idea"
                }}

    def register_user(self, user_details):
        """Sign up a new user to get a token"""
        register = self.client.post(self.signup_url,
                                    user_details,
                                    format='json')
        
        token = register.data["token"]
        return token

    def create_article(self, token):
        """Create an article."""
        response = self.client.post(
            self.create_article_url,
            self.create_article_data,
            format='json',
            HTTP_AUTHORIZATION='token {}'.format(token))
        slug = response.data['slug']
        return slug

    def test_comment_highlighted_text(self):
        """Test comment highlighted text."""
        token = self.register_user(self.user_two_details)
        slug = self.create_article(token)
        response = self.client.post(
            reverse('articles:high_light', kwargs={'slug': slug}),
            self.highlighted_text,
            HTTP_AUTHORIZATION='token {}'.format(token),
            format='json')
        self.assertIn('selected_text', response.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_rejects_start_index_larger_than_end_index(self):
        """Test rejects start index larger than end index."""
        token = self.register_user(self.user_two_details)
        slug = self.create_article(token)
        response = self.client.post(
            reverse('articles:high_light', kwargs={'slug': slug}),
            self.selection_start_index_larger_than_end_index,
            HTTP_AUTHORIZATION='token {}'.format(token),
            format='json')
        self.assertEqual(response.data['error'],
                         'The start_index_position should not '
                         'be greater or equal end_index_position')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_rejects_invalid_types_for_highlight_index(self):
        """Test rejects index data type that are not integers."""
        token = self.register_user(self.user_two_details)
        slug = self.create_article(token)
        response = self.client.post(
            reverse('articles:high_light', kwargs={'slug': slug}),
            self.invalid_index_datatype,
            HTTP_AUTHORIZATION='token {}'.format(token),
            format='json')
        self.assertEqual(response.data['error'],
                         'Start of highlight and end of highlight'
                         ' indices should be both integers')
        self.assertEqual(response.status_code,
                         status.HTTP_422_UNPROCESSABLE_ENTITY)

    def test_rejects_missing_required_field(self):
        """Test for missing field."""
        token = self.register_user(self.user_two_details)
        slug = self.create_article(token)
        response = self.client.post(
            reverse('articles:high_light', kwargs={'slug': slug}),
            self.missing_field,
            HTTP_AUTHORIZATION='token {}'.format(token),
            format='json')

        self.assertEqual(response.data['error'],
                         'start_highlight_position is required')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_all_comments(self):
        """Test get all comments."""
        token = self.register_user(self.user_two_details)

        # create an article
        response = self.client.post(
            self.create_article_url,
            self.create_article_data,
            format='json',
            HTTP_AUTHORIZATION='token {}'.format(token))
        slug = response.data['slug']
        
        # highlight a text and comment it
        self.client.post(
            reverse('articles:high_light', kwargs={'slug': slug}),
            self.highlighted_text,
            HTTP_AUTHORIZATION='token {}'.format(token),
            format='json')
        
        # get all comments
        response = self.client.get(
            reverse('articles:high_light', kwargs={'slug': slug}),
            format='json')
        response_data = json.loads(json.dumps(response.data))
        self.assertIn('selected_text', response_data[0])
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_get_single_comments(self):
        """Test get single comments."""
        token = self.register_user(self.user_two_details)

        # create an article
        response = self.client.post(
            self.create_article_url,
            self.create_article_data,
            format='json',
            HTTP_AUTHORIZATION='token {}'.format(token))
        slug = response.data['slug']
        
        # highlight a text and comment it
        response = self.client.post(
            reverse('articles:high_light', kwargs={'slug': slug}),
            self.highlighted_text,
            HTTP_AUTHORIZATION='token {}'.format(token),
            format='json')
        
        # get single comment
        article_id = response.data['id'] 
        response = self.client.get(
            '/api/articles/{}/highlight/{}'.format(slug, article_id),
            format='json')
        
        response_data = json.loads(json.dumps(response.data))
        self.assertIn('selected_text', response_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_delete_single_comments(self):
        """Test delete single comments."""

        token = self.register_user(self.user_two_details)

        # create an article
        response = self.client.post(
            self.create_article_url,
            self.create_article_data,
            format='json',
            HTTP_AUTHORIZATION='token {}'.format(token))
        slug = response.data['slug']
        
        # highlight a text and comment it
        response = self.client.post(
            reverse('articles:high_light', kwargs={'slug': slug}),
            self.highlighted_text,
            HTTP_AUTHORIZATION='token {}'.format(token),
            format='json')

        # delete single comment
        article_id = response.data['id'] 
        response = self.client.delete(
            '/api/articles/{}/highlight/{}'.format(slug, article_id),
            HTTP_AUTHORIZATION='token {}'.format(token),
            format='json')
        response_data = json.loads(json.dumps(response.data))
        self.assertEqual(response.data['message'],
                         'Comment on highligted text deleted successfully')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_update_single_comments(self):
        """Test update single comment."""
        token = self.register_user(self.user_two_details)

        # create an article
        response = self.client.post(
            self.create_article_url,
            self.create_article_data,
            format='json',
            HTTP_AUTHORIZATION='token {}'.format(token))
        slug = response.data['slug']

        # highlight a text and comment on it
        response = self.client.post(
            reverse('articles:high_light', kwargs={'slug': slug}),
            self.highlighted_text,
            HTTP_AUTHORIZATION='token {}'.format(token),
            format='json')
        article_id = response.data['id']

        # update the comment
        response = self.client.put(
            '/api/articles/{}/highlight/{}'.format(slug, article_id),
            self.update_comment,
            HTTP_AUTHORIZATION='token {}'.format(token),
            format='json')
        response_data = json.loads(json.dumps(response.data))
        self.assertIn('selected_text', response_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_unexisting_comments(self):
        """Test update unexisting comment."""
        token = self.register_user(self.user_two_details)

        # create an article
        response = self.client.post(
            self.create_article_url,
            self.create_article_data,
            format='json',
            HTTP_AUTHORIZATION='token {}'.format(token))
        slug = response.data['slug']

        # update the comment
        response = self.client.put(
            '/api/articles/{}/highlight/{}'.format(slug, 2),
            self.update_comment,
            HTTP_AUTHORIZATION='token {}'.format(token),
            format='json')
        response_data = json.loads(json.dumps(response.data))
        self.assertEqual(response.data['message'], 'Comment on selected text does not exist')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
    
    def test_get_delete_unexisting_comments(self):
        """Delete unexisting comment"""
        token = self.register_user(self.user_two_details)

        # create an article
        response = self.client.post(
            self.create_article_url,
            self.create_article_data,
            format='json',
            HTTP_AUTHORIZATION='token {}'.format(token))
        slug = response.data['slug']

        # update the comment
        response = self.client.delete(
            '/api/articles/{}/highlight/{}'.format(slug, 2),
            self.update_comment,
            HTTP_AUTHORIZATION='token {}'.format(token),
            format='json')
        response_data = json.loads(json.dumps(response.data))
        self.assertEqual(response.data["error"], "The comment does not exist")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

