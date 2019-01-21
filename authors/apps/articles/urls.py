from django.urls import path

from .views import ArticleAPIView, ArticleDetailsView, DeleteArticle

app_name = "articles"
urlpatterns = [
    path('articles/', ArticleAPIView.as_view(), name="articles-listcreate"),
    path('articles/<slug:slug>/',
         ArticleDetailsView.as_view(),
         name="articles-retrieveupdate"),
    path('articles/delete/<slug:slug>/',
         DeleteArticle.as_view(),
         name="articles-delete"),
]
