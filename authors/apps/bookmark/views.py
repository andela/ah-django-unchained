from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import (IsAuthenticatedOrReadOnly,
                                        IsAuthenticated)
from django.core.exceptions import ObjectDoesNotExist
from django.db.utils import IntegrityError
from ..articles.models import Article

from .serializers import BookmarksSerializer
from .models import Bookmarks


class CreateBookmark(generics.CreateAPIView, generics.DestroyAPIView):
    serializer_class = BookmarksSerializer
    queryset = Bookmarks.objects.all()
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def create(self, request, slug, *args, **kwargs):
        user = request.user
        try:
            article_instance = Article.objects.get(slug=slug)
        except ObjectDoesNotExist:
            return Response(
                {'error': 'Article {} does not exist'.format(slug)},
                status.HTTP_404_NOT_FOUND)
        data = {
            "article": article_instance.id,
            "user": user.id}
        serializer = self.serializer_class(data=data)
        try:
            serializer.is_valid(raise_exception=True)
            serializer.save()
        except IntegrityError:
            return Response(
                {'error': 'Article already exist in your bookmark'},
                status.HTTP_400_BAD_REQUEST)
        return Response(
            {'message': 'Article  has been added to your bookmark'},
            status.HTTP_201_CREATED)

    def destroy(self, request, slug, *args, **kwargs):
        article_instance = Article.objects.get(slug=slug)
        article_id = article_instance.id
        try:
            bookmark = Bookmarks.objects.get(article=article_id)
        except ObjectDoesNotExist:
            return Response(
                {'error': 'Article does not exist in your bookmark'},
                status.HTTP_404_NOT_FOUND)
        self.perform_destroy(bookmark)
        return Response(
            {'message': 'Article has been remove from your bookmark'})


class ListALlBookmarks(generics.ListAPIView):
    serializer_class = BookmarksSerializer
    queryset = Bookmarks.objects.all()
    permission_classes = (IsAuthenticated,)

    def list(self, request, *args, **kwargs):
        bookmark = Bookmarks.objects.filter(user=request.user)
        serializer = self.serializer_class(bookmark, many=True)
        data = serializer.data
        if len(data) == 0:
            return Response(
                {'my_bookmarks': []},
                status.HTTP_404_NOT_FOUND)
        for item in data:
            article_instance = Article.objects.get(pk=item['article'])
            item['title'] = article_instance.title
            item['slug'] = article_instance.slug
            item['description'] = article_instance.description
            item['user'] = request.user.username
        return Response({'my_bookmarks': data}, status.HTTP_200_OK)
