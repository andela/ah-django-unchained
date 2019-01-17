from django.http import Http404
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import generics
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from authors.apps.authentication.serializers import UserSerializer
from .models import Friend
from .serializers import CustomUserSerializer


class FollowApiView(generics.CreateAPIView):
    """view for following a user"""
    permission_classes = (IsAuthenticated,)

    def post(self, request, username, format=None):
        """
        This will check if the user associated with the username passed exists
        If true, it will check for the user sending the request
        If it's the same user, then an error message is returned
        Else the intermediary Friend model will be used to
        create the user relationship
        Finally the serialized object of the followed user is returned
        """
        try:
            followed = get_user_model().objects.get(username=username)
        except ObjectDoesNotExist:
            raise Http404()

        follower = get_user_model().objects.get(pk=request.user.id)

        if followed == follower:
            return Response(
                {"message": "You cannot follow yourself"},
                status=status.HTTP_406_NOT_ACCEPTABLE)
        Friend.objects.get_or_create(user_from=follower, user_to=followed)
        user = get_user_model().objects.get(pk=followed.id)
        serilizer = UserSerializer(user)
        if serilizer:
            return Response(serilizer.data, status=status.HTTP_200_OK)


class UnFollowApiView(generics.DestroyAPIView):
    """view for unfollowing a user"""
    permission_classes = (IsAuthenticated,)

    def delete(self, request, username, format=None):
        """
        This will check if the user associated with the username passed exists
        If true, it will check for the user sending the request
        If it's the same user, then an error message is returned
        Else the intermediary Friend model will be used to
        delete the user relationship
        Finally the serialized object of the unfollowed user is returned
        """
        try:
            followed = get_user_model().objects.get(username=username)
        except ObjectDoesNotExist:
            raise Http404()

        follower = get_user_model().objects.get(pk=request.user.id)

        if followed == follower:
            return Response(
                {"message": "you cannot follow yourself"},
                status=status.HTTP_406_NOT_ACCEPTABLE)
        Friend.objects.filter(user_from=follower, user_to=followed).delete()
        user = get_user_model().objects.get(pk=followed.id)
        serilizer = UserSerializer(user)
        if serilizer:
            return Response(serilizer.data, status=status.HTTP_200_OK)


class FollowersApiView(generics.ListAPIView):
    """view for listing all followers of a particular user"""

    def get_queryset(self):
        """
        check if the user associated with the username passed exists
        if true return all the friend objects associated with the user
        """
        user = get_object_or_404(
            get_user_model(), username=self.kwargs['username'])
        return Friend.objects.select_related(
            'user_from', 'user_to').filter(user_to=user.id).all()

    def get(self, request, username, format=None):
        """
            Get & return the followers from the respective
            object relationships i.e 'user_from'
        """
        friend_objects = self.get_queryset()
        if friend_objects is not None:
            followers = {u.user_from for u in friend_objects}
            serializer = CustomUserSerializer(followers, many=True)
            return Response(serializer.data)


class FollowingApiView(generics.ListAPIView):
    """views to get all users a user is following"""

    def get_queryset(self):
        """
        check if the user associated with the username passed exists
        if true return all the friend objects associated with the user
        """
        user = get_object_or_404(
            get_user_model(), username=self.kwargs['username'])
        return Friend.objects.select_related(
            'user_from', 'user_to', ).filter(user_from=user.id).all()

    def get(self, request, username, format=None):
        """
            Get & return the 'followed users' from the
            respective object relationships i.e 'user_to'
        """
        friend_objects = self.get_queryset()
        if friend_objects is not None:
            users_followed = {u.user_to for u in friend_objects}
            serializer = CustomUserSerializer(users_followed, many=True)
            return Response(serializer.data)
