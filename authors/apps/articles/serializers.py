from rest_framework import serializers
from authors.apps.profiles.serializers import UserProfileSerializer
from authors.apps.profiles.models import UserProfile
from .models import Article, Comment, HighlightTextModel

from taggit_serializer.serializers import (TagListSerializerField,
                                           TaggitSerializer)


class ArticleSerializer(TaggitSerializer, serializers.ModelSerializer):
    """Serializers for creating and retrieving all articles"""
    # Field in the database corresponding to the User model
    author = serializers.SerializerMethodField()
    # Uploads an image to the Cloudinary servers
    images = serializers.URLField(required=False)
    tagList = TagListSerializerField()
    user_id_likes = serializers.PrimaryKeyRelatedField(
        many=True, read_only=True)
    user_id_dislikes = serializers.PrimaryKeyRelatedField(
        many=True, read_only=True)

    likes_count = serializers.SerializerMethodField()
    dislikes_count = serializers.SerializerMethodField()
    # Field to favourite an article
    favorite = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = Article
        fields = ['title',
                  'slug',
                  'description',
                  'body',
                  'is_published',
                  'created',
                  'modified',
                  'images',
                  'author',
                  'slug',
                  'tagList',
                  'user_id_likes',
                  'user_id_dislikes',
                  'likes_count',
                  'dislikes_count',
                  'favorite']
        read_only_fields = ['created',
                            'modified',
                            'author',
                            'slug',
                            'images']

    # Inserts the ID of the author of an article into the foreign key row
    def get_author(self, obj):
        return obj.author.username

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
                  'is_published',
                  'slug',
                  'tagList',
                  'favorite']
        read_only_fields = ['modified',
                            'author',
                            'slug']

    """Get logged in user ID"""

    def get_author(self, obj):
        return obj.author.username


class DeleteArticleSerializer(serializers.ModelSerializer):
    """Serializer for deleting an article"""

    class Meta:
        model = Article
        fields = ['is_deleted']


class RatingSerializer(serializers.Serializer):
    """validate rating article"""
    rate = serializers.IntegerField(required=True)


class CommentSerializer(serializers.ModelSerializer):
    """Serializer for creating a Comment"""
    author = serializers.SerializerMethodField()
    body = serializers.CharField()
    user_id_likes = serializers.PrimaryKeyRelatedField(many=True,
                                                       read_only=True)
    user_id_dislikes = serializers.PrimaryKeyRelatedField(many=True,
                                                          read_only=True)
    likes_count = serializers.SerializerMethodField()
    dislikes_count = serializers.SerializerMethodField()

    def get_author(self, comment):
        author = UserProfileSerializer(comment.author.profile)
        return author.data

    def format_date(self, date):
        return date.strftime('%d %b %Y %H:%M:%S')

    # insert total likes
    def get_likes_count(self, obj):
        return obj.user_id_likes.count()

    # insert total dislikes
    def get_dislikes_count(self, obj):
        return obj.user_id_dislikes.count()

    def to_representation(self, instance):
        threads = [
            {
                'id': thread.id,
                'body': thread.body,
                'author': UserProfileSerializer(
                    instance=UserProfile.objects.get(user=thread.author)).data,
                'createdAt': self.format_date(thread.createdAt),
                'updatedAt': self.format_date(thread.updatedAt)
            } for thread in instance.threads.all()
        ]

        thread_comment = super(CommentSerializer, self).to_representation(
            instance)

        thread_comment['createdAt'] = self.format_date(instance.createdAt)
        thread_comment['updatedAt'] = self.format_date(instance.updatedAt)
        thread_comment['article'] = instance.article.title
        thread_comment['threads'] = threads
        del thread_comment['parent']

        return thread_comment

    class Meta:
        model = Comment
        fields = ('id', 'body', 'createdAt', 'updatedAt',
                  'author', 'parent', 'article', 'is_deleted',
                  'user_id_likes', 'user_id_dislikes',
                  'likes_count', 'dislikes_count')


class DeleteCommentSerializer(serializers.ModelSerializer):
    """Serializer for deleting an article"""

    class Meta:
        model = Comment
        fields = ['is_deleted', 'parent']


class SharingSerializer(serializers.Serializer):
    pass


class HighlightSerializer(serializers.Serializer):
    """Serializer for creating a Comment"""
    id = serializers.IntegerField(read_only=True)
    user_id = serializers.SerializerMethodField()
    article = serializers.SerializerMethodField()
    body = serializers.CharField()
    selected_text = serializers.CharField()
    start_highlight_position = serializers.IntegerField()
    end_highlight_position = serializers.IntegerField()

    def create(self, validated_data):
        return HighlightTextModel.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.body = validated_data.get('body', instance.body)
        instance.save()
        return instance

    def get_user_id(self, obj):
        return obj.user_id.id

    def get_article(self, obj):
        return obj.article.slug


class CommentHistorySerializer(serializers.Serializer):
    """Serializer for tracking comment edit history"""

    id = serializers.IntegerField()
    body = serializers.CharField()
    createdAt = serializers.CharField()
    updatedAt = serializers.CharField()


class PublishArticleSerializer(serializers.ModelSerializer):
    """Serializer for publishing an article"""

    class Meta:
        model = Article
        fields = ['is_published', ]
