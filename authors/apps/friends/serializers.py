from django.contrib.auth import get_user_model
from rest_framework import serializers


class CustomUserSerializer(serializers.ModelSerializer):
    """custom user serializer for getting usernames"""
    class Meta:
        model = get_user_model()
        fields = ('username',)
