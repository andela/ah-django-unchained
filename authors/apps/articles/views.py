import random

from django.template.defaultfilters import slugify
from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import (ListCreateAPIView,
                                     RetrieveUpdateAPIView, UpdateAPIView)
from rest_framework.permissions import (IsAuthenticated,
                                        IsAuthenticatedOrReadOnly)
from rest_framework.renderers import JSONRenderer
from authors.apps.core.permissions import IsAuthorOrReadOnly

from . import serializers
from .serializers import (ArticleSerializer,
                          GetArticleSerializer, DeleteArticleSerializer)
from .models import Article


class ArticleAPIView(ListCreateAPIView):
    """Creates articles and retrieves all articles"""
    permission_classes = (IsAuthenticatedOrReadOnly,)
    # Only fetch those articles whose 'is_deleted' field is True
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
    queryset = Article.objects.all()
    serializer_class = DeleteArticleSerializer
    lookup_field = 'slug'
