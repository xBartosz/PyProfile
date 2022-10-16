from django.urls import path

# from .controllers import PostsApiView
from .views import login_user, RegisterFunction, index, delete_post, update_post, like_post, detail_view, Report_function
from django.contrib.auth.views import LogoutView
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('', index, name='index'),


    path('login/', login_user, name='login'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    path('register/', RegisterFunction.as_view(), name='register'),

    path('reset_password', auth_views.PasswordResetView.as_view(template_name="website/reset_password.html"), name="reset_password"),
    path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(template_name="website/reset_password_sent.html"), name="reset_password_sent"),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name="password_reset_confirm"),
    path('reset_password_complete', auth_views.PasswordResetCompleteView.as_view(template_name="website/reset_password_complete.html"), name="password_reset_complete"),

    path('delete_post/<int:id>', delete_post, name='delete_post'),
    path('update_post/<int:id>', update_post, name='update_post'),
    path('report_post/<int:id>', Report_function, name='report_post'),
    path('like/<int:id>', like_post, name='like_post'),
    path('detail_view/<int:pk>', detail_view, name='detail_view'),
    # path('like/<int:pk>', LikeView, name='like_post'),
    # path('api/posts', PostsApiView.as_view()),
]