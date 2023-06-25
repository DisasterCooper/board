from django.shortcuts import render, redirect
from django.views import View, generic

from .forms import UserRegisterForm, UserRedactForm
from .models import User


class Registration(View):

    def get(self, request):
        return render(request, "registration/registration.html", {"form": UserRegisterForm()})

    def post(self, request):

        form = UserRegisterForm(request.POST)

        if not form.is_valid():
            return render(request, "registration/registration.html", {"form": form})

        form.save()
        return redirect("accounts:login")


class RedactUser(generic.UpdateView):
    model = User
    form_class = UserRedactForm
    pk_url_kwarg = "user_id"
    template_name = "user/redact_user.html"
