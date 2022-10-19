# Generated by Django 4.1 on 2022-10-18 21:46

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('website', '__first__'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('notifications', '0002_notify'),
    ]

    operations = [
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('notification_type', models.CharField(choices=[('Like', 'Like'), ('Comment', 'Comment'), ('Post', 'Post')], max_length=20)),
                ('notification_text', models.CharField(blank=True, max_length=50)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('is_seen', models.BooleanField(default=False)),
                ('post', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='notif_post', to='website.post')),
                ('receiver', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='notif_to_user', to=settings.AUTH_USER_MODEL)),
                ('sender', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='notif_from_user', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.DeleteModel(
            name='Notify',
        ),
        migrations.DeleteModel(
            name='TrainerNotification',
        ),
    ]