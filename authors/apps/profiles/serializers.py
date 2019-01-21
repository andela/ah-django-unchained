from rest_framework import serializers
from .models import UserProfile


class UserProfileSerializer(serializers.ModelSerializer):
    """
    Class to serialize user profile data
    """
    profile_image = serializers.ImageField(default=None)

    class Meta:
        model = UserProfile
        fields = ('first_name', 'last_name', 'gender', 'bio', 'profile_image')
