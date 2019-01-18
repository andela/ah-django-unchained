from rest_framework import status, generics, response
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.renderers import JSONRenderer
from authors.apps.core.permissions import IsAuthorOrReadOnly
from . import serializers
from .serializers import ArticleSerializer, GetArticleSerializer, DeleteArticleSerializer
from .models import Article

class ArticleAPIView(generics.ListCreateAPIView):
    permission_classes = (IsAuthenticatedOrReadOnly,)
    queryset = Article.objects.filter(is_dispayed=True)
    serializer_class = ArticleSerializer
    renderer_classes = (JSONRenderer,)
    
    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

class ArticleDetailsView(generics.RetrieveUpdateAPIView):
    """This class handles the http GET and PUT requests."""
    permission_classes = (IsAuthorOrReadOnly,)
    queryset = Article.objects.filter(is_dispayed=True)
    serializer_class = GetArticleSerializer
    lookup_field = 'slug'

class DeleteArticle(generics.UpdateAPIView):
    permission_classes = (IsAuthorOrReadOnly,)
    queryset = Article.objects.all()
    serializer_class = DeleteArticleSerializer
    lookup_field = 'slug'
