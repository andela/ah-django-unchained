from rest_framework import serializers
from .models import Bookmarks
from ..authentication.models import User


class BookmarksSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all()
    )

    class Meta:
        model = Bookmarks
        fields = ('user', 'article', 'created_at',)
        read_only_fields = ('created_at',)
