from django.urls import path

from .views import (ArticleAPIView, ArticleDetailsView,
                    DeleteArticle, LikeArticleApiView,
                    DislikeArticleApiView, PostRatingsAPIView,
                    FavoriteArticle, AverageRatingsAPIView,
                    CreateComment, CommentDetailsView,
                    CommentDelete, CommentsRetrieveUpdateDestroy,
                    ReadTime
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
         FavoriteArticle.as_view(),
         name="articles-favorite"),

    path('articles/<slug>/comments/<int:id>/',
         CommentDetailsView.as_view(), name="get_comments"),
    path('articles/<slug>/comments/add/<int:id>/',
         CommentsRetrieveUpdateDestroy.as_view(), name="create_thread_comments"),
    path('articles/<slug>/comments/delete/<int:id>/',
         CommentDelete.as_view(), name="delete_comments"),
    path('articles/<slug>/comments/',
         CreateComment.as_view(), name="create_comments"),
    path('articles/read/<slug:slug>/',
         name="articles_view_ratings")
    path('articles/read/<slug>/',
         ReadTime.as_view(),
         name="articles-read"),
]

