from rest_framework.generics import ListAPIView
from rest_framework_filters import filters
from .models import Article
from .serializers import  ArticleSerializer


class ArticleFilter(filters.FilterSet):
    author = filters.CharFilter(name='username')
    tags =filters.CharFilter(name='tags')
    title=filters.CharFilter(name='title')

    class Meta:
        model = Article
        fields = ['author', 'tags', 'title']


class FilterArticles(ListAPIView):
    filter_class = ArticleFilter
    serializer_class = ArticleSerializer
    queryset = Article.objects.all()

