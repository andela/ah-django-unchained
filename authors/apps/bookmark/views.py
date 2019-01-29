from rest_framework import generics
from rest_framework.response import Response
from .serializers import BookmarksSerializer


class BookmarkView(generics.CreateAPIView):
    serializer_class = BookmarksSerializer
    
    def post(self, request, slug,*args, **kwargs):
        article_instance = Article.objects.get('')
        return Response({'': slug})