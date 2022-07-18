from django_unicorn.components import UnicornView
from ..models import Post
from django.contrib.auth.models import User
from django.contrib import messages


class PostsView(UnicornView):
    author: User = None
    posts: Post = None
    content: str = ""


    def mount(self):
        self.author = User.objects.get(username=self.request.user)
        self.posts = Post.objects.all()
        return super().mount()

    def submit(self):
        if len(self.content) > 3:
            Post.objects.create(
                author=self.author,
                post_content=self.content
            )
            self.content = ""
            self.posts = Post.objects.all()
        else:
            messages.success(self.request, "Length of the comment must be at least 3 signs")
