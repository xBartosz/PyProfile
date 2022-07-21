from django import forms
# from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import Post, MyUser
#
class UserRegisterForm(UserCreationForm):

    class Meta:
        model = MyUser
        fields = ['email', 'first_name', 'last_name', 'mobile']


class PostForm(forms.ModelForm):
    post_content = forms.CharField(widget=forms.Textarea(attrs={
        'rows' : '4',
    }))

    class Meta:
        model = Post
        fields = ['post_content']

# class CustomLoginForm(AuthenticationForm):
#
#   def __init__(self, *args, **kwargs):
#     super().__init__(*args, **kwargs)
#     self.fields['username'].widget.attrs.update(
#       {'class': 'my-username-class'}
#     )
#     self.fields['password'].widget.attrs.update(
#       {'class': 'my-password-class'}
#     )
