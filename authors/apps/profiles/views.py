from rest_framework import generics
from .serializers import UserProfileSerializer
from ..authentication.models import User

class ProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = UserProfileSerializer
    queryset = User.objects.all()
