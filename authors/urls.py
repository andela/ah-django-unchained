"""authors URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.urls import include, path
from django.contrib import admin

# import from django_rest_swagger
from rest_framework_swagger.views import get_swagger_view

schema_view = get_swagger_view(title='Author\'s Haven API')

urlpatterns = [
    path('admin/', admin.site.urls),

    path('api/', include('authors.apps.authentication.urls',
                         namespace='authentication')),
    path('api/', include('authors.apps.friends.urls')),
    path('api/', include('authors.apps.profiles.urls', namespace='profiles')),

    path('api/', include('authors.apps.articles.urls', namespace='articles')),
    path('api/', include('authors.apps.bookmark.urls', namespace='bookmark')),
    path('api/', include('authors.apps.usernotifications.urls', namespace="notifications")),
    # Set the API documentation at the root of the site
    path('', schema_view)
]
