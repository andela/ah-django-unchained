from django.urls import path
from . import views


urlpatterns = [
    path(
        'profiles/<username>/follow',
        views.FollowUnfollowApiView.as_view(),
        name='follow'),
    path(
        'profiles/<username>/followers',
        views.FollowersApiView.as_view(),
        name='followers'),
    path(
        'profiles/<username>/following',
        views.FollowingApiView.as_view(),
        name='following'),
]
