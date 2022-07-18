from django.urls import path
from .views import LoginFunction, RegisterFunction, index
from django.contrib.auth.views import LogoutView


urlpatterns = [
    path('', index, name='index'),
    path('login/', LoginFunction.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    path('register/', RegisterFunction.as_view(), name='register')
]