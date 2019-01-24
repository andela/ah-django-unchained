from rest_framework import generics, status
from rest_framework.response import Response
from django.core.exceptions import ObjectDoesNotExist
from .serializers import UserProfileSerializer
from .models import UserProfile


class ProfileView(generics.RetrieveUpdateAPIView):
    '''
    class view to update user profile
    '''
    serializer_class = UserProfileSerializer
    queryset = UserProfile.objects.all()

    def update(self, request, username, *args, **kwargs):
        try:
            user_instance = UserProfile.objects.select_related(
                'user').get(user__username=username)
            if user_instance.user.username != request.user.username:
                return Response({'error': 'You are not allowed to edit or delete this object'}, status.HTTP_403_FORBIDDEN)
        except ObjectDoesNotExist:
            return Response({'error': 'Username {} not found'.format(username)}, status.HTTP_404_NOT_FOUND)
        serializer = self.serializer_class(
            instance=user_instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'message': serializer.data}, status.HTTP_200_OK)

    def retrieve(self, request, username, *args, **kwargs):
        try:
            user_instance = UserProfile.objects.select_related(
                'user').get(user__username=username)
        except ObjectDoesNotExist:
            return Response({'error': 'Username {} not found'.format(username)}, status.HTTP_404_NOT_FOUND)
        serializer = self.serializer_class(user_instance)
        return Response({'profile': serializer.data}, status.HTTP_200_OK)
