from django.urls import path
from .views import BookmarkView


app_name = "bookmarks"
urlpatterns = [
    path('article/<slug>/bookmark/', BookmarkView.as_view(), name='bookmark'),
]
