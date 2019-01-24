import re

from rest_framework import serializers
from .models import Article

from taggit_serializer.serializers import (TagListSerializerField,
                                           TaggitSerializer)


class ArticleSerializer(TaggitSerializer, serializers.ModelSerializer):
    """Serializers for creating and retrieving all articles"""
    # Field in the database corresponding to the User model
    author = serializers.SerializerMethodField()
    # Uploads an image to the Cloudinary servers
    images = serializers.ImageField(default=None)
    tagList = TagListSerializerField()
    likes = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    dislikes = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    all_likes = serializers.SerializerMethodField()
    all_dislikes = serializers.SerializerMethodField()

    class Meta:
        model = Article
        fields = ['title',
                  'slug',
                  'description',
                  'body',
                  'created',
                  'modified',
                  'images',
                  'author',
                  'slug',
                  'tagList'
                  'likes',
                  'dislikes',
                  'all_likes',
                  'all_dislikes']
        read_only_fields = ['created',
                            'modified',
                            'author',
                            'slug',
                            'images']

    # Inserts the ID of the author of an article into the foreign key row
    def get_author(self, obj):
        return obj.author.id

    # insert total likes
    def get_all_likes(self, obj):
        return obj.likes.count()

    # insert total dislikes
    def get_all_dislikes(self, obj):
        return obj.dislikes.count()


class GetArticleSerializer(serializers.ModelSerializer):
    """Serializers for retrieving a single article and updating"""
    # Field in the database corresponding to the User model
    author = serializers.SerializerMethodField()
    # Uploads an image to the Cloudinary servers
    images = serializers.ImageField(default=None)
    tagList = TagListSerializerField()

    class Meta:
        model = Article
        fields = ['title',
                  'description',
                  'body',
                  'modified',
                  'images',
                  'author',
                  'slug',
                  'tagList']
        read_only_fields = ['modified',
                            'author',
                            'slug']

    def get_author(self, obj):
        return obj.author.id


class DeleteArticleSerializer(serializers.ModelSerializer):
    """Serializer for deleting an article"""
    class Meta:
        model = Article
        fields = ['is_deleted']
