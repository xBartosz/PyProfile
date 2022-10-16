from django.urls import path
from .views import profile_settings, users_profile, friend_request, search_users, friend_list, post_list

urlpatterns = [
    path('profile_settings/', profile_settings, name='profile_settings'),
    path('profile/<str:username>', users_profile, name='profile'),
    path('friend_request/', friend_request, name='friend_request'),
    path('search_users/', search_users, name='search_users'),
    path('profile/<str:username>/friends', friend_list, name='friend_list'),
    path('profile/<str:username>/posts', post_list, name='post_list')

]