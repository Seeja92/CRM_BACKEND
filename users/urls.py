from django.urls import path
from django.contrib.auth import get_user_model
from .views import User

from .views import RegisterView, LoginView, LogoutView,UsersListView,admin_exists

urlpatterns = [
     path("admin-exists/", admin_exists),
    path('register/', RegisterView.as_view(), name='register'),
    path('login/',    LoginView.as_view(),    name='login'),
    path('logout/',   LogoutView.as_view(),   name='logout'),
    path('users/',    UsersListView.as_view(), name='users-list'),
]