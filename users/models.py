from django.db import models
# from django.contrib.auth.models import User
from PIL import Image
from website.views import RegisterFunction
from website.models import MyUser
import users.models
from django.dispatch import receiver
from django.db.models.signals import post_save

# Create your models here.

Genders = [('Female', 'Female'),
           ('Male', 'Male')]

Options = [('False', 'False'),
           ('True', 'True')]
class Profile(models.Model):
    user = models.OneToOneField(MyUser, null=True, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=45)
    last_name = models.CharField(max_length=60)
    profile_picture = models.ImageField(default='profile_pics/Default.jpg', upload_to='profile_pics')
    comes_from = models.CharField(max_length = 60, blank=True, null=True)
    birth_date = models.DateField(blank=True, null=True)
    about_me = models.TextField(blank=True, null=True)
    gender = models.CharField(max_length=60, blank=True, null=True, choices=Genders)
    mobile = models.CharField(max_length=50, blank=True, null=True)
    email_visibility = models.CharField(max_length=6, default=Options[0], choices=Options)
    mobile_visibility = models.CharField(max_length=6, default=Options[0], choices=Options)

    def __str__(self):
        return f'{self.user.first_name} {self.user.last_name}'




    def save(self,*args, **kwargs):
        super().save()

        img = Image.open(self.profile_picture.path)

        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.profile_picture.path)



@receiver(post_save, sender=MyUser)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance, first_name=instance.first_name, last_name=instance.last_name)
@receiver(post_save, sender=Profile)
def update_profile(sender, instance, created, **kwargs):
    if not created:
        MyUser.objects.filter(id=instance.id).update(first_name=instance.first_name, last_name=instance.last_name)


# class CustomUser(AbstractUser):
#     is_active = models.BooleanField(default=False)
#     profile_picture = models.ImageField(default='default.jpg', upload_to='profile_pics')