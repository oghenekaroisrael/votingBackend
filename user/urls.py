from django.urls import include, path
from . import views
from .views import register, login, logout
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('welcome', views.welcome),
    path('profile', views.get_profile),
    path('profile/<int:user_id>', views.update_profile),
    path('register', views.register),
    path('login', views.login),
    path('logout', views.logout),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
