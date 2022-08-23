from django.contrib import admin
from .models import Friend_Request
#
# # Register your models here.
#
#
# class FriendListAdmin(admin.ModelAdmin):
#     list_filter = ['user']
#     list_display = ['user']
#     search_fields = ['user']
#     readonly_fields = ['user']
#
#     class Meta:
#         model = FriendList
#
# admin.site.register(FriendList, FriendListAdmin)
#
# class FriendRequestAdmin(admin.ModelAdmin):
#     list_filter = ['sender', 'receiver']
#     list_display = ['sender', 'receiver']
#     search_fields = ['sender__username', 'sender__email', 'receiver__username', 'receiver__email']
#
#     class Meta:
#         model = FriendRequest



admin.site.register(Friend_Request)