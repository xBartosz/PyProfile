from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.utils.text import slugify

class CustomUserManager(BaseUserManager):

    def _create_user(self, email, password, first_name, last_name, mobile, **extra_fields):
        if not email:
            raise ValueError("Email must be provided")
        if not password:
            raise ValueError("Password is not provided")

        user = self.model(
            email= self.normalize_email(email),
            first_name = first_name,
            last_name = last_name,
            mobile = mobile,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password, first_name, last_name, mobile, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password,first_name, last_name, mobile, **extra_fields)

    def create_superuser(self, email, password, first_name, last_name, mobile, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('is_superuser', True)
        return self._create_user(email, password, first_name, last_name, mobile, **extra_fields)


class MyUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(db_index=True, unique=True, max_length=254)
    first_name = models.CharField(max_length=240)
    last_name = models.CharField(max_length=240)
    mobile = models.CharField(max_length=50)


    is_staff = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)

    objects= CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'mobile']


# class Author(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     slug = models.SlugField()
#
#     def __str__(self):
#         return self.user.username
#
#     def save(self, *args, **kwargs):
#         if not self.slug:
#             self.slug = slugify(self.user.username)
#         return super().save(*args, **kwargs)



class Post(models.Model):
    author = models.OneToOneField(MyUser, on_delete=models.CASCADE)
    post_content = models.TextField(blank=False, null=False)
    post_date = models.DateTimeField(auto_now_add=True)

class Reply_for_post(models.Model):
    author = models.OneToOneField(MyUser, on_delete=models.CASCADE)
    reply_content = models.TextField(blank=False, null=False)
    reply_date = models.DateTimeField(auto_now_add=True)