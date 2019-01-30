import json
from django.urls import reverse
from rest_framework.views import status
from rest_framework.test import APITestCase, APIClient


class CommentsTestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.signup_url = reverse('authentication:auth-register')
        self.create_article_url = reverse('articles:articles-listcreate')
        self.user_one_details = {
            "user": {
                "username": "mary123",
                "email": "mary123@andela.com",
                "password": "Password@123"
                }}
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
            "start_highlighting": 1,
            "end_highlighting": 5,
            "body": "Remove this from your code"
        }
        self.selection_out_of_range = {
            "start_highlighting": 1,
            "end_highlighting": 10,
            "body": "Remove this from your code"
        }
        self.selection_start_index_larger_than_end_index = {
            "start_highlighting": 5,
            "end_highlighting": 4,
            "body": "Remove this from your code"
        }
        self.invalid_index_datatype = {
            "start_highlighting": "one",
            "end_highlighting": 4,
            "body": "Remove this from your code"
        }
        self.missing_field = {
            "end_highlighting": 4,
            "body": "Remove this from your code"
        }

    def register_user(self, user_details):
        """Sign up a new user to get a token"""
        register = self.client.post(self.signup_url,
                                    user_details,
                                    format='json')
        token = register.data["token"]
        return token

    def create_article(self):
        """Create an article."""
        token = self.register_user(self.user_one_details)
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
        slug = self.create_article()
        response = self.client.post(
            reverse('articles:high_light', kwargs={'slug': slug}),
            self.highlighted_text,
            HTTP_AUTHORIZATION='token {}'.format(token),
            format='json')
        self.assertIn('selected_text', response.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_rejects_selection_out_of_range(self):
        """Test rejects selection that is out of range."""
        token = self.register_user(self.user_two_details)
        slug = self.create_article()
        response = self.client.post(
            reverse('articles:high_light', kwargs={'slug': slug}),
            self.selection_out_of_range,
            HTTP_AUTHORIZATION='token {}'.format(token),
            format='json')
        self.assertEqual(response.data['error'],
                         'Selection out of range.Selection'
                         ' should be between 0 and 6')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_rejects_start_index_larger_than_end_index(self):
        """Test rejects start index larger than end index."""
        token = self.register_user(self.user_two_details)
        slug = self.create_article()
        response = self.client.post(
            reverse('articles:high_light', kwargs={'slug': slug}),
            self.selection_start_index_larger_than_end_index,
            HTTP_AUTHORIZATION='token {}'.format(token),
            format='json')
        self.assertEqual(response.data['error'],
                         'The index of highlight start should '
                         'not be greater or equal highlight end')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_rejects_invalid_types_for_highlight_index(self):
        """Test rejects index data type that are not integers."""
        token = self.register_user(self.user_two_details)
        slug = self.create_article()
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
        """Test test for missing field."""
        token = self.register_user(self.user_two_details)
        slug = self.create_article()
        response = self.client.post(
            reverse('articles:high_light', kwargs={'slug': slug}),
            self.missing_field,
            HTTP_AUTHORIZATION='token {}'.format(token),
            format='json')

        self.assertEqual(response.data['error'],
                         'start_highlighting is required')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
