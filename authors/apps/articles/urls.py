from django.urls import path

from .views import (ArticleAPIView, ArticleDetailsView,
                    DeleteArticle, LikeArticleApiView,
                    DislikeArticleApiView, PostRatingsAPIView,
                    AverageRatingsAPIView, FaveArticle
                    )


app_name = "articles"
urlpatterns = [
    path('articles/', ArticleAPIView.as_view(), name="articles-listcreate"),
    path('articles/<slug:slug>/',
         ArticleDetailsView.as_view(),
         name="articles-retrieveupdate"),
    path('articles/delete/<slug>/',
         DeleteArticle.as_view(),
         name="articles-delete"),
    path('articles/<slug>/like/',
         LikeArticleApiView.as_view(), name='likes'),
    path('articles/<slug>/dislike/',
         DislikeArticleApiView.as_view(), name='dislikes'),
    path('articles/<slug>/rate/',
         PostRatingsAPIView.as_view(),
         name="rate_article"),
    path('articles/rate/<slug>/',
         AverageRatingsAPIView.as_view(),
         name="articles_view_ratings"),
    path('articles/<slug>/favorite',
          FaveArticle.as_view(),
          name="articles-favorite")
]
