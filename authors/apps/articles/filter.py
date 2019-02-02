from django_filters import rest_framework as filters
from rest_framework.generics import ListAPIView
from .serializers import ArticleSerializer
from .models import Article


class ArticleFilter(filters.FilterSet):
    author = filters.CharFilter(field_name='author__username',
                                lookup_expr='icontains')
    title = filters.CharFilter(field_name='title', lookup_expr='icontains')
    tags = filters.CharFilter(field_name='tagList', method='get_tags')

    def get_tags(self, queryset, name, value):
        return queryset.filter(tagList__name__icontains=value)

    class Meta:
        model = Article
        fields = ['author', 'title', 'tags']


class FilterArticles(ListAPIView):
    serializer_class = ArticleSerializer
    queryset = Article.objects.filter(is_deleted=False)
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = ArticleFilter
