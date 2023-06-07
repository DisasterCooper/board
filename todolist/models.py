from django.db import models


class Post(models.Model):
    title = models.CharField(max_length=200)  # null = False по умолчанию
    created = models.DateTimeField(auto_now_add=True)
    content = models.TextField()
    # tag = models.CharField(max_length=50)
    user = models.ForeignKey("user.User", on_delete=models.CASCADE, related_name="posts")

    class Meta:
        ordering = ["created"]

    @property
    def comments_count(self) -> int:
        return self.comments.all().count()


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
    username = models.CharField(max_length=100)
    email = models.EmailField()
    content = models.TextField()
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["created"]
