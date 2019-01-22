from django.urls import reverse
from rest_framework.test import APIClient, APITestCase
from rest_framework import status


class TestArticleRatings(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.register_url = reverse('authentication:auth-register')
        self.login_url = reverse("authentication:auth-login")
        self.rating_url = reverse(
            "articles: articles-listcreate",
            kwargs={'slug': 'your-first-blog'})

        self.rating_non_existing_url = reverse(
            "articles:rate-article", kwargs={'slug': 'your-second-blog'})

        self.username = "testuser"
        self.email = "testuser@gmail.com"
        self.password = "this_user123@A"

        self.test_user = User.objects.create_user(
            username=self.username,
            email=self.email,
            password=self.password)

        self.data_for_test = {"user": {
            "email": self.email,
            "password": self.password
        }}

        login_res = self.client.post(
            self.login_url, self.data_for_test, format='json')
        self.assertEqual(login_res.status_code, status.HTTP_200_OK)
        self.token = login_res.data["token"]

        def create_article(self):
            article_details = dict(article=dict(
                title="your first blog",
                description='this is your first blog',
                body='this is your first blog'
                ))
            self.client.post(
                reverse("articles:articles-listcreate"),
                data=json.dumps(article_details),
                content_type="application/json",
                HTTP_AUTHORIZATION='Token ' + self.token)

    def test_rate_article(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        response = self.client.post(self.rating_url, data={"rating": 4})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_rate_with_number_outside_range(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        response = self.client.post(self.rating_url, data={"rating": 6},)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.data['message'], 'Give a rating between 1 to 5 inclusive')

    def test_rate_with_non_numeric(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        response = self.client.post(self.rating_url, data={"rating": "a"})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.data['message'], 'Only integers, 1 to 5 are allowed')

    def test_rate_non_existing_article(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        response = self.client.post(
            self.rating_non_existing_url, data={"rating": 4})
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data["message"], 'Article not found')

    def test_rating_by_unauthenticated_user(self):
        response = self.client.post(
            self.rating_url, data={"rating": 4})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.data["message"], 'Please sign in')

    def test_rate_with_empty_rating(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        response = self.client.post(self.rating_url, data={"rating": {}})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.data["message"], 'Please provide a rating between 1 to 5')
