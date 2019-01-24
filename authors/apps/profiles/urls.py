from django.urls import path
from .views import ProfileView


app_name = "profiles"
urlpatterns = [
    path('profiles/<username>/', ProfileView.as_view(), name='put-profile'),
]
