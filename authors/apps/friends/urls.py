from django.urls import path
from . import views


urlpatterns = [
    path(
        'users/<username>/follow',
        views.FollowApiView.as_view(),
        name='follow'),
    path(
        'users/<username>/unfollow',
        views.UnFollowApiView.as_view(),
        name='unfollow'),
    path(
        'users/<username>/followers',
        views.FollowersApiView.as_view(),
        name='followers'),
    path(
        'users/<username>/following',
        views.FollowingApiView.as_view(),
        name='following'),
]
