from rest_framework import serializers
from ..authentication.models import User

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('gender', 'bio', 'profile_image')

