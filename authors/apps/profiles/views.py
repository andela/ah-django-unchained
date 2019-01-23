from rest_framework import generics, status
from rest_framework.response import Response
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
                return Response({'response':'You are not allowed to edit or delete this object'})
        except:
            return Response({'response': 'Username {} not found'.format(username)}, status.HTTP_404_NOT_FOUND)
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.update(instance=user_instance, validated_data=request.data)
        return Response({'response': 'profile has been updated successfully '})

    def retrieve(self, request, username, *args, **kwargs):
        try:
            user_instance = UserProfile.objects.select_related(
                'user').get(user__username=username)
        except:
            return Response({'': ''}, status.HTTP_404_NOT_FOUND)
        serializer = self.serializer_class(user_instance)
        return Response({'profile': serializer.data})
