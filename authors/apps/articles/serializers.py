from rest_framework import serializers
from .models import Article


class ArticleSerializer(serializers.ModelSerializer):
    # Field in the database corresponding to the User model
    author = serializers.SerializerMethodField()
    # Uploads an image to the Cloudinary servers
    images = serializers.ImageField()

    class Meta:
        model = Article
        fields = ['title', 'slug', 'description', 'body', 'created', 'modified', 'images', 'author']
        read_only_fields = ['created', 'modified', 'author', 'slug']

    # Inserts the ID of the author of an article into the foreign key row
    def get_author(self,obj):
        return obj.author.id
