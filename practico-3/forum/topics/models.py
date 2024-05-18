from django.db import models

class Topic(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Response(models.Model):
    topic = models.ForeignKey(Topic, related_name='responses', on_delete=models.CASCADE)
    content = models.TextField()
    author_name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)


