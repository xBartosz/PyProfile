from django.db import models
# from django.contrib.auth.models import User
from PIL import Image
from website.models import MyUser
from django.dispatch import receiver
from django.db.models.signals import post_save

# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(MyUser, null=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=45)
    last_name = models.CharField(max_length=60)
    profile_picture = models.ImageField(default='profile_pics/Default.jpg', upload_to='profile_pics')

    def __str__(self):
        return f'{self.user.first_name} {self.user.last_name}'

    # def save(self,*args, **kwargs):
    #     super().save()
    #
    #     img = Image.open(self.profile_picture.path)
    #
    #     if img.height > 300 or img.width > 300:
    #         output_size = (300, 300)
    #         img.thumbnail(output_size)
    #         img.save(self.profile_picture.path)


@receiver(post_save, sender=MyUser)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

# class CustomUser(AbstractUser):
#     is_active = models.BooleanField(default=False)
#     profile_picture = models.ImageField(default='default.jpg', upload_to='profile_pics')