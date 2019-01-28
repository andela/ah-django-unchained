import random

from django.template.defaultfilters import slugify
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import get_object_or_404
from django.core import serializers
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.renderers import JSONRenderer
from rest_framework.generics import (ListCreateAPIView,
                                     RetrieveUpdateDestroyAPIView,
                                     RetrieveUpdateAPIView,
                                     UpdateAPIView, CreateAPIView,
                                     DestroyAPIView)

from rest_framework.permissions import (IsAuthenticated,
                                        IsAuthenticatedOrReadOnly)
from rest_framework.exceptions import NotFound, ValidationError
from rest_framework import status
from authors.apps.core.permissions import IsAuthorOrReadOnly
from .serializers import (ArticleSerializer,
                          GetArticleSerializer, DeleteArticleSerializer,
                          RatingSerializer, CommentSerializer,
                          DeleteCommentSerializer)
from .models import (Article, ArticleRating, Comment)


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

    def get(self, request, slug, *args, **kwargs):
        """Retrieve a single article"""
        article = get_object_or_404(Article, slug=self.kwargs["slug"])
        serializer = self.serializer_class(article)
        return set_favorite_status(serializer, self.request.user.id)


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


class AverageRatingsAPIView(APIView):
    """
    Class for viewing article ratings
    """

    serializer_class = RatingSerializer

    def get(self, request, slug):
        """method for viewing average ratings"""
        rate = 0

        try:
            article = Article.objects.get(slug=slug)
        except ObjectDoesNotExist:
            raise NotFound('article not found')

        rate_articles = ArticleRating.objects.filter(article=article)

        for rate_article in rate_articles:
            rate += rate_article.rate
        rate_value = 0
        if rate:
            rate_value = rate / rate_articles.count()
        return Response(
            data={"ratings": round(rate_value, 1)}, status=status.HTTP_200_OK)


class PostRatingsAPIView(CreateAPIView):
    """
    Class for rating an article
    """
    permission_classes = (IsAuthenticated,)
    serializer_class = RatingSerializer

    def post(self, request, slug):
        """method for posting a rating"""
        data = request.data
        serializer = self.serializer_class(data=data)
        serializer.is_valid(raise_exception=True)

        if not int(data['rate']) > 0 or not int(data['rate']) <= 5:
            return Response(
                {"message": "Give a rating between 1 to 5 inclusive"},
                status=status.HTTP_400_BAD_REQUEST
                )

        try:
            article = Article.objects.get(slug=slug)
        except ObjectDoesNotExist:
            raise NotFound('Article not found')

        author = article.author.id
        if author == request.user.id:
            return Response(
                {"error": "You are not allowed to rate your own article"},
                status=status.HTTP_400_BAD_REQUEST)

        user = request.user
        response = Response(
                {
                    "message": "Article successfully rated",
                    "rating": serializer.data['rate']
                },
                status=status.HTTP_201_CREATED
                )

        # update the rating if there's one
        try:
            article_ratings = ArticleRating.objects.get(
                user=user, article=article
                )
            article_ratings.rate = data['rate']
            article_ratings.save()
            return response
        # create new rating if none exists
        except ArticleRating.DoesNotExist:
            article_ratings = ArticleRating(
                user=user, article=article, rate=data['rate']
                )
            article_ratings.save()
            return response


class FavoriteArticle(CreateAPIView, DestroyAPIView):
    """Favorite an Article."""
    permission_classes = (IsAuthenticated,)
    serializer_class = ArticleSerializer

    def post(self, request, slug):
        try:
            # get an article that matches the slug specified
            # and return a message if the article does not exist
            article = Article.objects.get(slug=slug)
        except ObjectDoesNotExist:
            raise NotFound("This article does not exist")

        # check if the article has been favorited by the current user
        # if it is favorited we return a message saying it is
        if article in Article.objects.filter(favorite=request.user):
            message = {'message': 'Article already favorited.'}
            return Response(message)

        # If it is not favorited we favorite the article
        article.favorite.add(request.user)

        serializer = self.serializer_class(article,
                                           context={'request': request},
                                           partial=True)

        return set_favorite_status(serializer, self.request.user.id)

    def delete(self, request, slug):
        try:
            # get an article that matches the slug specified
            # and return a message if the article does not exist
            article = Article.objects.get(slug=slug)
        except ObjectDoesNotExist:
            raise NotFound("This article does not exist")

        # check if the article has been favorited by the current user
        # if it is we unfavorited it
        if article in Article.objects.filter(favorite=request.user):
            article.favorite.remove(request.user)
            serializer = self.serializer_class(article,
                                               context={'request': request},
                                               partial=True)

            return set_favorite_status(serializer, self.request.user.id)

        # If it is unfavorited we return a message saying it is unfavorited
        return Response({'message': 'Article already unfavorited.'})


def set_favorite_status(data, user):
        """Set the favorite value to either True or False"""
        # Check if the user has favorited the article
        value = [value for value in data.data['favorite'] if
                 user in data.data['favorite']]
        # Article has not been favorited, set favorite to False
        if not value:
            serialized_details = data.data
            serialized_details['favorite'] = False
            return Response(serialized_details, status.HTTP_200_OK)
        # Article has not been favorited, set favorite to True
        serialized_details = data.data
        serialized_details['favorite'] = True
        return Response(serialized_details)


class CommentDelete(UpdateAPIView):

    """This class Deletes Comments created by the a particular user"""
    permission_classes = (IsAuthorOrReadOnly,)
    queryset = Comment.objects.filter(is_deleted=False)
    serializer_class = DeleteCommentSerializer
    lookup_field = 'id'


class CommentDetailsView(RetrieveUpdateAPIView):
    """This class handles the http GET and PUT requests."""
    permission_classes = (IsAuthorOrReadOnly,)
    queryset = Comment.objects.filter(is_deleted=False)
    serializer_class = CommentSerializer
    lookup_field = 'id'


class CreateComment(ListCreateAPIView):
    """This class Creates comments."""
    serializer_class = CommentSerializer
    queryset = Comment.objects.filter(is_deleted=False)
    permission_classes = (IsAuthenticated, )

    def post(self, request, slug, *args, **kwargs):
        article = Article.objects.filter(slug=slug, is_deleted=False).first()
        serializer_context = {
            'request': request,
            'author': request.user,
            'article': get_object_or_404(Article, slug=self.kwargs["slug"])
        }
        serializer = CommentSerializer(data=request.data, context=serializer_context)
        if serializer.is_valid():
            serializer.save(author=request.user, article_id=article.id)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CommentsRetrieveUpdateDestroy(RetrieveUpdateDestroyAPIView, CreateAPIView):
    serializer_class = CommentSerializer
    permission_classes = (IsAuthenticated,)
    queryset = Comment.objects.filter(is_deleted=False)
    lookup_field = 'id'

    def create(self, request, slug, id):
        """Method for creating a child comment on parent comment."""

        context = super(CommentsRetrieveUpdateDestroy,
                        self).get_serializer_context()

        comment = Comment.objects.filter(id=id, is_deleted=True).first()
        if comment:
            message = {'error': 'Comment has been deleted'}
            return Response(message, status=status.HTTP_404_NOT_FOUND)
        article = Article.objects.get(slug=slug)
        if isinstance(article, dict):
            return Response(article, status=status.HTTP_404_NOT_FOUND)
        parent = article.comments.get(id=id).pk

        if not parent:
            message = {'error': 'Comment not found.'}
            return Response(message, status=status.HTTP_404_NOT_FOUND)
        body = request.data.get('body', {})

        data = {
            'body': body,
            'parent': parent,
            'article': article.pk,
        }

        serializer = self.serializer_class(
            data=data, context=context)
        serializer.is_valid(raise_exception=True)
        serializer.save(author=self.request.user, article_id=article.pk)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
