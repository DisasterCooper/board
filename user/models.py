from django.db import models
from django.contrib.auth.models import AbstractUser


class Avatar(models.Model):
    image = models.ImageField(upload_to="media/avatars")


class User(AbstractUser, models.Model):
    phone = models.CharField(max_length=20, null=True)
    address = models.CharField(max_length=150, null=True)
    avatar_image = models.ForeignKey(
        Avatar,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name="users"
    )

    class Meta:
        db_table = "user"
        # abstract = True
