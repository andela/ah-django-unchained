import jwt

from django.conf import settings
from django.shortcuts import get_object_or_404
from django.http import Http404

from rest_framework import status
from rest_framework.generics import (
    ListAPIView,
    ListCreateAPIView,
    DestroyAPIView,
    UpdateAPIView
    )
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from .serializers import NotificationSerializer, UnsubscribeSerializer
from authors.apps.authentication.models import User


class NotificationAPIView(ListAPIView, DestroyAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = NotificationSerializer

    def get(self, request, *args, **kwargs):
        notifications = self.notifications(request)
        serializer = self.serializer_class(
            notifications, many=True, context={'request': request}
            )

        return Response(
            {"count": notifications.count(), "notifications": serializer.data}
            )

    def notifications(self, request):
        # this method will be overriden by the following methods
        pass


class AllNotificationsAPIView(NotificationAPIView):
    """
    list all the notifications for this user
    """
    def notifications(self, request):
        request.user.notifications.mark_as_sent()
        return request.user.notifications.active()


class UnsubscribeAPIView(ListAPIView, UpdateAPIView):
    """
    class for allowing users to unsubscribe from notifications
    """
    permission_classes = [AllowAny]
    serializer_class = UnsubscribeSerializer

    def get(self, request, token):
        """
        unsubscribe from email notifications
        """
        try:
            email = jwt.decode(token, settings.SECRET_KEY)['email']
            user = User.objects.get(email=email)
        except(TypeError, ValueError, OverflowError, Exception):
            raise Http404

        user.email_notification_subscription = False
        user.save()
        message = {
            "message": "You have successfully unsubscribed from notifications",
            "email": user.email_notification_subscription,
            "app": user.app_notification_subscription
        }
        return Response(message, status=status.HTTP_200_OK)

    def put(self, request):
        """
        unsubscribe from app notifications
        """
        self.permission_classes.append(IsAuthenticated)
        user = get_object_or_404(User, email=request.user.email)
        user.app_notification_subscription = False
        message = {
            "message": "You have successfully unsubscribed from notifications",
            "email": user.email_notification_subscription,
            "app": user.app_notification_subscription
        }
        return Response(message, status=status.HTTP_200_OK)


class SubscribeAPIView(ListCreateAPIView, UpdateAPIView):
    """
    allow users to subscribe to nofications
    """
    permission_classes = [IsAuthenticated]

    def post(self, request):
        """
        subscribe to all notifications
        """
        user = get_object_or_404(User, email=request.user.email)
        user.email_notification_subscription = True
        user.app_notification_subscription = True
        user.save()
        message = {
            "message": "You have successfully subscribed to notifications",
            "email": user.email_notification_subscription,
            "app": user.app_notification_subscription
        }
        return Response(message, status=status.HTTP_200_OK)
