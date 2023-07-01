from avatar.models import Avatar
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.shortcuts import reverse


class User(AbstractUser, models.Model):
    avatar_image = models.ImageField(upload_to="media/avatars")
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

    def get_absolute_url(self):  # надо ли прописывать???
        return reverse("avatar_add", args=[str(self.id)])  # что вытягивать?
