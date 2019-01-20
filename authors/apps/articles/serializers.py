import re

from rest_framework import serializers
from .models import Article

class ArticleSerializer(serializers.ModelSerializer):
    """Serializers for creating and retrieving all articles"""
    # Field in the database corresponding to the User model
    author = serializers.SerializerMethodField()
    # Uploads an image to the Cloudinary servers
    images = serializers.ImageField(default=None)
    

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
                  'slug']
        read_only_fields = ['created',
                            'modified',
                            'author',
                            'slug',
                            'images']

    # Inserts the ID of the author of an article into the foreign key row
    def get_author(self,obj):
        return obj.author.id

class GetArticleSerializer(serializers.ModelSerializer):
    """Serializers for retrieving a single article and updating"""
    # Field in the database corresponding to the User model
    author = serializers.SerializerMethodField()
    # Uploads an image to the Cloudinary servers
    images = serializers.ImageField(default=None)

    class Meta:
        model = Article
        fields = ['title',
                  'description',
                  'body',
                  'modified',
                  'images',
                  'author',
                  'slug']
        read_only_fields = ['modified',
                            'author',
                            'slug']

    def get_author(self,obj):
        return obj.author.id

class DeleteArticleSerializer(serializers.ModelSerializer):
    """Serializer for deleting an article"""
    class Meta:
        model = Article
        fields = ['is_displayed']
