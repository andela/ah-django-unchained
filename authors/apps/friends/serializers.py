import json
from django.contrib.auth import get_user_model
from rest_framework import serializers


class FollowersFollowingSerializer(serializers.ModelSerializer):
    """custom user serializer for getting usernames"""
    class Meta:
        model = get_user_model()
        fields = ('username',)


class FollowUnfollowSerializer(serializers.ModelSerializer):
    """
    custom user serializer for getting id, username, number of
    followers, and followinng
    """
    number_of_following = serializers.SerializerMethodField()
    number_of_followers = serializers.SerializerMethodField()

    class Meta:
        model = get_user_model()
        fields = (
            'id', 'username', "number_of_followers", "number_of_following"
            )

    def get_number_of_followers(self, obj):
        return len(
            json.loads(json.dumps([u.username for u in obj.followers.all()]))
            )

    def get_number_of_following(self, obj):
        return len(
            json.loads(json.dumps([u.username for u in obj.following.all()]))
            )
