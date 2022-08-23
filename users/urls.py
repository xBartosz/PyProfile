from django.urls import path
from .views import profile_settings, users_profile, friend_request, search_users

urlpatterns = [
    path('profile_settings/', profile_settings, name='profile_settings'),
    path('profile/<int:user_id>', users_profile, name='profile'),
    path('friend_request/', friend_request, name='friend_request'),
    path('search_users/', search_users, name='search_users')

]