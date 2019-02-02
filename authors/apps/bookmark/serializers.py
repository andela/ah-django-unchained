from rest_framework import serializers
from .models import Bookmarks
from ..authentication.models import User
from ..articles.models import Article


class BookmarksSerializer(serializers.Serializer):
    user = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all()
    )
    article = serializers.PrimaryKeyRelatedField(
        queryset=Article.objects.all()
    )

    def create(self, validated_data):
        return Bookmarks.objects.create(**validated_data)
