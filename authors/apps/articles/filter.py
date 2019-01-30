from rest_framework.generics import ListAPIView
from django_filters.rest_framework import DjangoFilterBackend
from django_filters import rest_framework as filters
from .serializers import ArticleSerializer
from .models import Article


class ArticleFilter(filters.FilterSet):
    author = filters.CharFilter(field_name='author__username',
                                lookup_expr='exact')
    title = filters.CharFilter(field_name='title', lookup_expr='exact')
    tagList = filters.CharFilter(field_name='tagList', lookup_expr='exact')

    class Meta:
        model = Article
        fields = ['author', 'title', 'tagList']


class FilterArticles(ListAPIView):
    serializer_class = ArticleSerializer
    queryset = Article.objects.all()
    filter_backends = (DjangoFilterBackend,)
    filterset_class = ArticleFilter
