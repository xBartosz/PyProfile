from django.db import models
from datetime import datetime
# Create your models here.

class Message(models.Model):
    context = models.TextField()
    date = models.DateTimeField(default=datetime.now, blank=True)