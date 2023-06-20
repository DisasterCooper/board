from django.shortcuts import render, redirect
from django.views import View

from .forms import UserRegisterForm, UserChangeForm
from .models import User


class Registration(View):

    def get(self, request):
        return render(request, "registration/registration.html", {"form": UserRegisterForm()})

    def post(self, request):

        form = UserRegisterForm(request.POST)

        if not form.is_valid():
            return render(request, "registration/registration.html", {"form": form})

        form.save()
        return redirect("accounts: login")


class ShowUser(View):
    pass


class RedactUser(View):
    model = User

    def get(self, request):
        user = request.user
        return render(request, "user/redact_user.html", {"user_form": UserChangeForm()})

    def post(self, request):
        form = UserRegisterForm(request.POST)

        if not form.is_valid():
            return render(request, "registration/registration.html", {"form": form})

        form.save()
        return redirect("accounts: login")
