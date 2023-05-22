from django.db import models


class Post(models.Model):
    title = models.CharField(max_length=200)  # null = False по умолчанию
    created = models.DateTimeField(auto_now_add=True)
    content = models.TextField()
    # tag = models.CharField(max_length=50)
