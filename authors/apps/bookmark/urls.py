from django.urls import path
from .views import CreateBookmark, ListALlBookmarks


app_name = "bookmarks"
urlpatterns = [
    path(
        'article/<slug>/bookmark/',
        CreateBookmark.as_view(), name='edit-bookmark'),
    path('article/bookmark/', ListALlBookmarks.as_view(), name='bookmarks'),
]
