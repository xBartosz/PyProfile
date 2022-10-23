from django.contrib import admin
from .models import Post, MyUser, Reply_for_post, Report_post, Likes
# Register your models here.

admin.site.register(Post)
admin.site.register(Reply_for_post)
admin.site.register(MyUser)
admin.site.register(Report_post)
admin.site.register(Likes)
# admin.site.register(Author)