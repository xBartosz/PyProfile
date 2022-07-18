from django.contrib import admin
from .models import Profile
# Register your models here.

admin.site.register(Profile)


from django.contrib import admin
# from django.contrib.auth.admin import UserAdmin
#
# from .models import CustomUser
#
# class CustomUserAdmin(UserAdmin):
#     list_display = (
#         'username', 'email', 'first_name', 'last_name', 'is_staff',
#         'is_active', 'profile_picture'
#         )
#
#     fieldsets = (
#         (None, {
#             'fields': ('username', 'password')
#         }),
#         ('Personal info', {
#             'fields': ('first_name', 'last_name', 'email')
#         }),
#         ('Permissions', {
#             'fields': (
#                 'is_active', 'is_staff', 'is_superuser',
#                 'groups', 'user_permissions'
#                 )
#         }),
#         ('Important dates', {
#             'fields': ('last_login', 'date_joined')
#         }),
#
#     )
#
#     add_fieldsets = (
#         (None, {
#             'fields': ('username', 'password1', 'password2')
#         }),
#         ('Personal info', {
#             'fields': ('first_name', 'last_name', 'email')
#         }),
#         ('Permissions', {
#             'fields': (
#                 'is_active', 'is_staff', 'is_superuser',
#                 'groups', 'user_permissions'
#                 )
#         }),
#         ('Important dates', {
#             'fields': ('last_login', 'date_joined')
#         }),
#
#     )
#
# admin.site.register(CustomUser, CustomUserAdmin)