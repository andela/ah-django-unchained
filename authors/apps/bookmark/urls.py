from django.urls import path
from .views import CreateBookmark, ListALlBookmarks, DeleteBookmark


app_name = "bookmarks"
urlpatterns = [
    path('article/<slug>/create/bookmark/', CreateBookmark.as_view(), name='create-bookmark'),
    path('article/<slug>/delete/bookmark/', DeleteBookmark.as_view(), name='delete-bookmark'),
    path('article/bookmark/', ListALlBookmarks.as_view(), name='bookmarks'),
]
