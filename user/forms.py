from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django import forms
from captcha.fields import CaptchaField

from .models import User


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    captcha = CaptchaField()
    avatar_image = forms.ImageField(required=False)

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2", "avatar_image"]


class UserRedactForm(UserChangeForm):
    email = forms.EmailField(required=True)
    captcha = CaptchaField()
    avatar_image = forms.ImageField(required=False)

    class Meta:
        model = get_user_model()
        fields = "__all__"
