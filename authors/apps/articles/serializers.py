import re

from rest_framework import serializers
from .models import Article, ArticleRating

from taggit_serializer.serializers import (TagListSerializerField,
                                           TaggitSerializer)


class ArticleSerializer(TaggitSerializer, serializers.ModelSerializer):
    """Serializers for creating and retrieving all articles"""
    # Field in the database corresponding to the User model
    author = serializers.SerializerMethodField()
    # Uploads an image to the Cloudinary servers
    images = serializers.ImageField(default=None)
    tagList = TagListSerializerField()
    user_id_likes = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    user_id_dislikes = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    likes_count = serializers.SerializerMethodField()
    dislikes_count = serializers.SerializerMethodField()

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
                  'tagList',
                  'user_id_likes',
                  'user_id_dislikes',
                  'likes_count',
                  'dislikes_count']
        read_only_fields = ['created',
                            'modified',
                            'author',
                            'slug',
                            'images']

    # Inserts the ID of the author of an article into the foreign key row
    def get_author(self, obj):
        return obj.author.id

    # insert total likes
    def get_likes_count(self, obj):
        return obj.user_id_likes.count()

    # insert total dislikes
    def get_dislikes_count(self, obj):
        return obj.user_id_dislikes.count()


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


class RatingSerializer(serializers.Serializer):
    """validate rating article"""
    rate = serializers.IntegerField(required=True)

    def validate(self, data):
        rate = data['rate']
        if not int(rate) > 0 or not int(rate) <= 5:
            raise serializers.ValidationError(
                'Give a rating between 1 to 5 inclusive'
                )
        return data
