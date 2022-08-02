from django.urls import path
from .views import LoginFunction, RegisterFunction, index
from django.contrib.auth.views import LogoutView
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('', index, name='index'),
    path('login/', LoginFunction.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    path('register/', RegisterFunction.as_view(), name='register'),

    path('reset_password', auth_views.PasswordResetView.as_view(template_name="website/reset_password.html"), name="reset_password"),
    path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(template_name="website/reset_password_sent.html"), name="reset_password_sent"),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name="password_reset_confirm"),
    path('reset_password_complete', auth_views.PasswordResetCompleteView.as_view(template_name="website/reset_password_complete.html"), name="password_reset_complete"),

    # path('like/<int:pk>', LikeView, name='like_post'),
]