from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Post

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class PostForm(forms.ModelForm):
    post_content = forms.CharField(widget=forms.Textarea(attrs={
        'rows' : '4',
    }))

    class Meta:
        model = Post
        fields = ['post_content']