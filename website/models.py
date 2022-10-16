from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.utils.text import slugify
from django.contrib.humanize.templatetags.humanize import naturaltime
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

class CustomUserManager(BaseUserManager):

    def _create_user(self, email, user_name, password, first_name, last_name, **extra_fields):
        if not email:
            raise ValueError("Email must be provided")
        if not password:
            raise ValueError("Password is not provided")

        user = self.model(
            email=self.normalize_email(email),
            user_name = user_name,
            first_name = first_name,
            last_name = last_name,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, user_name, password, first_name, last_name, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, user_name, password, first_name, last_name, **extra_fields)

    def create_superuser(self, email, user_name, password, first_name, last_name, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('is_superuser', True)
        return self._create_user(email, user_name, password, first_name, last_name, **extra_fields)


# class CustomUserManager(BaseUserManager):
#     def create_user(self, email, user_name, first_name, last_name, password=None):
#         if not email:
#             raise ValueError("Users must have an email address. ")
#         user = self.model(
#             email=self.normalize_email(email).lower(),
#             user_name = user_name,
#             first_name = first_name,
#             last_name = last_name
#         )
#         user.set_password(password)
#         user.save(using=self._db)
#         return user
#
#     def create_superuser(self, email, user_name, first_name, last_name, password):
#         user = self.create_user(
#             email = self.normalize_email(email).lower(),
#             user_name = user_name,
#             first_name = first_name,
#             last_name = last_name,
#             password = password
#         )
#         user.is_admin = True
#         user.is_staff = True
#         user.is_superuser = True
#         user.save(using=self._db)
#         return user


class MyUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(db_index=True, unique=True, max_length=254)
    user_name = models.CharField(max_length=50, unique=True)
    first_name = models.CharField(max_length=240)
    last_name = models.CharField(max_length=240)
    friends = models.ManyToManyField('self', blank=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    # last_online = models.DateTimeField(blank=True, null=True)
    is_staff = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['user_name', 'first_name', 'last_name']


    #
    # # In this method, check that the date of the last visit is not older than 15 minutes
    # def is_online(self):
    #     if self.last_online:
    #         return (timezone.now() - self.last_online) < timezone.timedelta(minutes=15)
    #     return False
    #
    #
    # # If the user visited the site no more than 15 minutes ago,
    # def get_online_info(self):
    #     if self.is_online():
    #         # then we return information that he is online
    #         return _('Online')
    #     if self.last_online:
    #         # otherwise we write a message about the last visit
    #         return _('Last visit {}').format(naturaltime(self.last_online))
    #         # If you have only recently added information about a user visiting the site
    #         # then for some users there may not be any information about the visit, we will return information that the last visit is unknown
    #     return _('Unknown')



class Post(models.Model):
    author = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    post_content = models.TextField(blank=True)
    post_date = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(MyUser, related_name='post_likes', blank=True)
    edited = models.BooleanField(default=False)

    def count_likes(self):
        return self.likes.count()
    # likes = models.ManyToManyField(MyUser, related_name='posts', null=True, blank=True)

    # def save(self, *args, **kwargs):
    #     super(Post, self).save(*args, **kwargs)
    # def total_likes(self):
    #     return self.likes.count()


class Reply_for_post(models.Model):
    post = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE)
    reply_author = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    reply_content = models.TextField(blank=False, null=False)
    reply_date = models.DateTimeField(auto_now_add=True)


Report_post_reasons = [('Spam', 'Spam'),
                       ('Nudity', 'Nudity'),
                       ('Violence', 'Violence'),
                       ('Harassment', 'Harassment'),
                       ('Suicide', 'Suicide'),
                       ('Self-Injury', 'Self-Injury'),
                       ('False News', 'False News'),
                       ('Hate Speech', 'Hate Speech'),
                       ('Terrorism', 'Terrorism'),

                       ]

class Report_post(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    applicant = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    reason = models.CharField(max_length=50, choices=Report_post_reasons)
    report_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.post}, {self.reason}'
