from django_unicorn.components import UnicornView
from ..models import Post, MyUser
# from django.contrib.auth.models import User
from django.contrib import messages


class PostsView(UnicornView):
    author: MyUser = None
    posts: Post = None
    content: str = ""


    def mount(self):
        self.author = MyUser.objects.get(email=self.request.user)
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
