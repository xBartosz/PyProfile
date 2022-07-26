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

class CustomRegisterForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].widget.attrs.update(
            {'class' : 'my-email-class'}
        )
        self.fields['first_name'].widget.attrs.update(
            {'class': 'my-firstname-class'}
        )
        self.fields['last_name'].widget.attrs.update(
            {'class': 'my-lastname-class'}
        )
        self.fields['mobile'].widget.attrs.update(
            {'class': 'my-mobile-class'}
        )
        self.fields['password1'].widget.attrs.update(
            {'class': 'my-password1-class'}
        )
        self.fields['password2'].widget.attrs.update(
            {'class': 'my-password2-class'}
        )