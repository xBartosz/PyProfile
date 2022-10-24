from django import forms
# from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import Post, MyUser, ReplyForPost, ReportPost
from django import forms


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = MyUser
        fields = ['email', 'first_name', 'last_name']

    def clean_email(self):
        email = self.cleaned_data.get("email")
        return email


class PostForm(forms.ModelForm):
    post_content = forms.CharField(widget=forms.Textarea(attrs={
        'rows' : '4',
    }))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['post_content'].widget.attrs.update(
            {'class': 'my-post-content-class'}
        )

    class Meta:
        model = Post
        fields = ['post_content']


class PostLike(forms.ModelForm):

    class Meta:
        model = Post
        fields = ['likes']


class ReplyForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['reply_content'].widget.attrs.update(
            {'class': 'my-reply-content-class'}
        )

    class Meta:
        model = ReplyForPost
        fields = ['reply_content']


class ReportForm(forms.ModelForm):
    class Meta:
        model = ReportPost
        fields = ['reason']
