from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import  IsAuthenticatedOrReadOnly
from django.core.exceptions import ObjectDoesNotExist
from ..articles.models import Article

from .serializers import BookmarksSerializer
from .models import Bookmarks


class BookmarkView(generics.CreateAPIView):
    serializer_class = BookmarksSerializer
    queryset = Bookmarks.objects.all()
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def post(self, request, slug, *args, **kwargs):
        user=request.user
        try:
            article_instance = Article.objects.get(slug=slug)
        except ObjectDoesNotExist:
            return Response({'error': 'article {} does not exist'.format(slug)},status.HTTP_404_NOT_FOUND)
        data = {"article": article_instance.id, "user": user.id}
        import pdb; pdb.set_trace()
        serializer = self.serializer_class(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'': serializer.data})

