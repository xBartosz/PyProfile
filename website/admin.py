from django.contrib import admin
from .models import Post, MyUser, ReplyForPost, ReportPost, Likes
# Register your models here.

admin.site.register(Post)
admin.site.register(ReplyForPost)
admin.site.register(MyUser)
admin.site.register(ReportPost)
admin.site.register(Likes)
# admin.site.register(Author)