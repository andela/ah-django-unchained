from django.urls import path


from .views import ProfileView

app_name = "profiles"
urlpatterns = [
    path('profile/<int:pk>/', ProfileView.as_view()),
]
