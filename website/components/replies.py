from django_unicorn.components import UnicornView
from website.models import Post, MyUser, Reply_for_post
from django.contrib import messages


class RepliesView(UnicornView):
    reply_author: MyUser = None
    reply: Reply_for_post = None
    reply_content: str = ""


    def mount(self):
        self.reply_author = MyUser.objects.get(email=self.request.user)
        self.reply = Reply_for_post.objects.all()
        return super().mount()

    def reply_submit(self):
        # print(self.request.POST.get("post_id"))
        if len(self.reply_content) > 3:
            Reply_for_post.objects.create(

                reply_author=self.reply_author,
                reply_content=self.reply_content
            )
            self.reply_content = ""
            self.reply = Reply_for_post.objects.all()
        else:
            messages.success(self.request, "Length of the comment must be at least 3 signs")


