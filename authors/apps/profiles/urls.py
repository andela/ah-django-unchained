from django.urls import path
from .views import ProfileView, GetProfileView


app_name = "profiles"
urlpatterns = [
    path('profiles/<slug:slug>/', ProfileView.as_view(), name='post-profile'),
    path('profiles/<slug:slug>/', GetProfileView.as_view(), name='get-profile'),
]
