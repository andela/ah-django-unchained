from django.urls import path
from .views import ProfileView, GetProfileView


app_name = "profiles"
urlpatterns = [
    path('profile/<slug:slug>/', ProfileView.as_view(), name='post-profile'),
    path('profile/<slug:slug>/', GetProfileView.as_view(), name='get-profile'),
]
