from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django import forms
from captcha.fields import CaptchaField

from .models import User


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    captcha = CaptchaField()
    avatar = forms.ImageField(required=False)

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2", "avatar"]


# class UserRedactForm(UserChangeForm):
# #     email = forms.EmailField(required=True)
# #     captcha = CaptchaField()
# #     avatar = forms.ImageField(required=True)
# #
# #     class Meta:
# #         model = User
        # fields = ["username", "email", "password1", "password2", "avatar"]
