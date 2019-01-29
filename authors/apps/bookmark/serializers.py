from rest_framework import serializers
from .models import Bookmarks


class BookmarksSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bookmarks
        fields = ('user', 'article', 'updated_at', 'created_at',)
        read_only_fields = ('updated_at', 'created_at',)