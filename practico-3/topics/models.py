from django.db import models
from django.contrib.auth.models import User

class Topic(models.Model):
    title=  models.CharField(max_length=255)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now = True)
    user = models.TextField()

class Reply (models.Model):
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    user = models.TextField()
