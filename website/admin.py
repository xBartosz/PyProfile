from django.contrib import admin
from .models import Post, MyUser, Reply_for_post
# Register your models here.

admin.site.register(Post)
admin.site.register(Reply_for_post)
admin.site.register(MyUser)
# admin.site.register(Author)