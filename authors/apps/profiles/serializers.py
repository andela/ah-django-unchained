from rest_framework import serializers
from .models import UserProfile


class UserProfileSerializer(serializers.ModelSerializer):
    """
    Class to serialize user profile data
    """
    profile_image = serializers.ImageField(default='No image')
    gender = serializers.RegexField(
        regex='^(N|F|M)$',
        write_only=True,
        error_messages={
            'invalid': 'Please enter M if you are male, F if you are female or N if you do not want to disclose '
        }
    )

    class Meta:
        model = UserProfile
        fields = ('first_name', 'last_name', 'gender',
                  'bio', 'profile_image', 'updated_at')
        read_only_fields = ('updated_at',)

    def validate(self, data):
        first_name = data.get('first_name', None)
        last_name = data.get('last_name', None)
        email = data.get('email', None)
        bio = data.get('bio', None)
        gender = data.get('gender', None)
        if first_name is None:
            raise serializers.ValidationError('first name was not provided')
        if first_name is None:
            raise serializers.ValidationError('last name was not provided')
        return data
