from rest_framework import generics
from .serializers import UserProfileSerializer
from .models import UserProfile
from authors.apps.core.permissions import IsMyProfileOrReadOnly


class ProfileView(generics.RetrieveUpdateAPIView):
    """
    class view to update user profile
    """
    serializer_class = UserProfileSerializer
    queryset = UserProfile.objects.all()
    permission_classes = (IsMyProfileOrReadOnly,)
    lookup_field = 'slug'

class GetProfileView(generics.ListAPIView):
    """
    class view to view user profile
    """
    serializer_class = UserProfileSerializer
    queryset = UserProfile.objects.all()
    lookup_field = 'slug'
