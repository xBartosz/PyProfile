from django.urls import path
from .views import profile_settings, users_profile, users_list, search_users

urlpatterns = [
    path('profile_settings/', profile_settings, name='profile_settings'),
    path('profile/<int:user_id>', users_profile, name='profile'),
    path('users_list/', users_list, name='allusers'),
    path('search_users/', search_users, name='search_users')

]