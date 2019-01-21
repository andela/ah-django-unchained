from django.urls import path
from .views import ProfileView


app_name = "profiles"
urlpatterns = [
    path('profiles/<str:username>/', ProfileView.as_view(), name='put-profile'),
]
