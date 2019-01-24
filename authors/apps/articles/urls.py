from django.urls import path

from .views import (ArticleAPIView, ArticleDetailsView,
                    DeleteArticle, LikeArticleApiView, DislikeArticleApiView)
app_name = "articles"
urlpatterns = [
    path('articles/', ArticleAPIView.as_view(), name="articles-listcreate"),
    path('articles/<slug:slug>/',
         ArticleDetailsView.as_view(),
         name="articles-retrieveupdate"),
    path('articles/delete/<slug:slug>/',
         DeleteArticle.as_view(),
         name="articles-delete"),
    path('<slug>/like/', LikeArticleApiView.as_view(), name='likes'),
    path('<slug>/dislike/', DislikeArticleApiView.as_view(), name='dislikes')
]
