from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.db.models.signals import post_save, post_delete
from notifications.models import Notification


class CustomUserManager(BaseUserManager):

    def _create_user(self, email, user_name, password, first_name, last_name, **extra_fields):
        if not email:
            raise ValueError("Email must be provided")
        if not password:
            raise ValueError("Password is not provided")

        user = self.model(
            email=self.normalize_email(email),
            user_name=user_name,
            first_name=first_name,
            last_name=last_name,
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


class MyUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(db_index=True, unique=True, max_length=254)
    user_name = models.CharField(max_length=50, unique=True)
    first_name = models.CharField(max_length=240)
    last_name = models.CharField(max_length=240)
    friends = models.ManyToManyField('self', blank=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    is_staff = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['user_name', 'first_name', 'last_name']


class Post(models.Model):
    author = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    post_content = models.TextField(blank=True)
    post_date = models.DateTimeField(auto_now_add=True)
    edited = models.BooleanField(default=False)
    likes = models.IntegerField(default=0)
    user_likes = models.ManyToManyField(MyUser, related_name='user_likes')

    def count_likes(self):
        return self.likes.count()



    def user_created_post(sender, instance, created, *args, **kwargs):
        if created:
            Post = instance
            post = Post
            sender = post.author
            # notification_text =f'just add a new post {Post.post_content[:50]}'
            notification_text =f'just add a new post'
            friends = sender.friends.all()

            for friend in friends:
                notify = Notification(post=post, sender=sender, receiver=friend, notification_text=notification_text,
                                      notification_type="Post")
                notify.save()

    def user_deleted_post(sender, instance, *args, **kwargs):
        Post = instance
        post = Post
        sender = Post.author

        notify = Notification.objects.filter(post=post, sender=sender, notification_type="Post")
        notify.delete()


post_save.connect(Post.user_created_post, sender=Post)
post_delete.connect(Post.user_deleted_post, sender=Post)


class ReplyForPost(models.Model):
    post = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE)
    reply_author = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    reply_content = models.TextField(blank=False, null=False)
    reply_date = models.DateTimeField(auto_now_add=True)

    def user_comment_post(sender, instance, *args, **kwargs):
        reply_for_post = instance
        post = reply_for_post.post
        sender = reply_for_post.reply_author
        receiver = post.author
        # notification_text = f'just comment your post {reply_for_post.reply_content[:50]}'
        notification_text = f'just comment your post'
        if sender != receiver:
            notify = Notification(post=post, sender=sender, receiver=receiver, notification_text=notification_text,
                                  notification_type="Comment")
            notify.save()

    def user_deleted_comment(sender, instance, *args, **kwargs):
        reply_for_post = instance
        post = reply_for_post.post
        sender = reply_for_post.reply_author

        notify = Notification.objects.filter(post=post, sender=sender, notification_type="Comment")
        notify.delete()


post_save.connect(ReplyForPost.user_comment_post, sender=ReplyForPost)
post_delete.connect(ReplyForPost.user_deleted_comment, sender=ReplyForPost)


class Likes(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="reference_to_post")
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE, related_name="user_like")

    def user_liked_post(sender, instance, *args, **kwargs):
        like = instance
        post = like.post
        sender = like.user
        notification_text = f'just liked your post'
        receiver = post.author

        if sender != receiver:
            notify = Notification(post=post, sender=sender, receiver=receiver, notification_text=notification_text,
                                  notification_type="Like")
            notify.save()

    def user_unliked_post(sender, instance, *args, **kwargs):
        like = instance
        post = like.post
        sender = like.user
        receiver = post.author

        if sender != receiver:
            notify = Notification.objects.filter(post=post, sender=sender,
                                                 notification_type="Like")
            notify.delete()


post_save.connect(Likes.user_liked_post, sender=Likes)
post_delete.connect(Likes.user_unliked_post, sender=Likes)


class ReportPost(models.Model):
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

    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    applicant = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    reason = models.CharField(max_length=50, choices=Report_post_reasons)
    report_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.post}, {self.reason}'
