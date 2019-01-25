import random

from django.template.defaultfilters import slugify
from django.core.exceptions import ObjectDoesNotExist
from django.core import serializers
from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import (ListCreateAPIView,
                                     RetrieveUpdateAPIView, UpdateAPIView)
from rest_framework.permissions import (IsAuthenticated,
                                        IsAuthenticatedOrReadOnly)
from rest_framework.exceptions import NotFound

from authors.apps.core.permissions import IsAuthorOrReadOnly
from . import serializers
from .serializers import (ArticleSerializer,
                          GetArticleSerializer, DeleteArticleSerializer)
from .models import Article


class ArticleAPIView(ListCreateAPIView):
    """Creates articles and retrieves all articles"""
    permission_classes = (IsAuthenticatedOrReadOnly,)
    # Only fetch those articles whose 'is_deleted' field is False
    queryset = Article.objects.filter(is_deleted=False)
    serializer_class = ArticleSerializer

    def post(self, request):
        # Create unique slugs based on the article title
        slug = slugify(request.data['title'])
        new_slug = slug
        random_num = random.randint(1, 10000)
        # Checks if the slug name already exists
        # If it does, append a randomly generated number at the end of the slug
        while Article.objects.filter(slug=new_slug).exists():
            new_slug = '{}-{}'.format(slug, random_num)
            random_num += 1
        slug = new_slug
        article = request.data
        serializer = self.serializer_class(data=article)
        if serializer.is_valid():
            serializer.save(author=self.request.user, slug=slug)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ArticleDetailsView(RetrieveUpdateAPIView):
    """This class handles the http GET and PUT requests."""
    permission_classes = (IsAuthorOrReadOnly,)
    queryset = Article.objects.filter(is_deleted=False)
    serializer_class = GetArticleSerializer
    lookup_field = 'slug'


class DeleteArticle(UpdateAPIView):
    permission_classes = (IsAuthorOrReadOnly,)
    queryset = Article.objects.filter(is_deleted=False)
    serializer_class = DeleteArticleSerializer
    lookup_field = 'slug'


class LikeArticleApiView(ListCreateAPIView):
    """Like an article."""
    permission_classes = (IsAuthenticatedOrReadOnly, )
    serializer_class = ArticleSerializer

    def put(self, request, slug):
        try:
            # get an article with the specified slug
            # and return a message if the article does not exist
            single_article_instance = Article.objects.get(slug=slug)
        except ObjectDoesNotExist:
            raise NotFound("An article with this slug does not exist")

        # check if the article has been disliked by the current user
        # if the current user has disliked it, then the dislike status
        # is set to null
        if single_article_instance in Article.objects.filter(
                                        user_id_dislikes=request.user):
            single_article_instance.user_id_dislikes.remove(request.user)

        # if the current user had previously liked this article,
        # then the article is unliked
        if single_article_instance in Article.objects.filter(
                                        user_id_likes=request.user):
            single_article_instance.user_id_likes.remove(request.user)

        # updating the article's like status to 1 for the
        # current user
        else:
            single_article_instance.user_id_likes.add(request.user)

        serializer = self.serializer_class(single_article_instance,
                                           context={'request': request},
                                           partial=True)
        return Response(serializer.data, status.HTTP_200_OK)


class DislikeArticleApiView(ListCreateAPIView):
    """Dislike an Article."""
    permission_classes = (IsAuthenticatedOrReadOnly,)
    serializer_class = ArticleSerializer

    def put(self, request, slug):
        try:
            # get an article that matches the specified slug
            # and return a message if the article does not exist
            single_article_instance = Article.objects.get(slug=slug)
        except ObjectDoesNotExist:
            raise NotFound("An article with this slug does not exist")

        # check if the article has been liked by the current user
        # if the current user has liked then the like status
        # is set to null
        if single_article_instance in Article.objects.filter(
                                        user_id_likes=request.user):
            single_article_instance.user_id_likes.remove(request.user)

        # if the current user had previously disliked this article,
        # then the dislike status of article is set to none
        if single_article_instance in Article.objects.filter(
                                        user_id_dislikes=request.user):
            single_article_instance.user_id_dislikes.remove(request.user)

        # updating the article's dislike status to 1 for the
        # current user
        else:
            single_article_instance.user_id_dislikes.add(request.user)

        serializer = self.serializer_class(single_article_instance,
                                           context={'request': request},
                                           partial=True)
        return Response(serializer.data, status.HTTP_200_OK)
