import notifications.urls
from django.urls import path, include

from . import views

app_name = "notifications"

urlpatterns = [
    path(
        'notifications/all/',
        views.AllNotificationsAPIView.as_view(),
        name="all-notifications"
        ),
    path(
        'notifications/unsubscribe/<token>',
        views.UnsubscribeAPIView.as_view(),
        name="email-unsubscribe"
        ),
    path(
        'notifications/unsubscribe/',
        views.UnsubscribeAPIView.as_view(),
        name="app-unsubscribe"
        ),
    path(
        'notifications/subscribe/',
        views.SubscribeAPIView.as_view(),
        name="subscribe"
        )
]
