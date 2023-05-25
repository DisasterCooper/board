from django.shortcuts import render, redirect, get_object_or_404, reverse
from django.http import HttpResponseNotAllowed
from django.views import View

from .models import Post


class PostsList(View):

    @staticmethod
    def get_queryset():
        return Post.objects.all()

    def get(self, request):
        posts = self.get_queryset()  # QuerySet все заметки
        return render(request, "home.html", {"posts": posts})


class PostValidate:

    @classmethod
    def is_valid(cls, title: str, content: str) -> bool:
        return cls.validate_title(title) and cls.validate_content(content)

    @staticmethod
    def validate_title(title: str) -> bool:
        pass

    @staticmethod
    def validate_content(content: str) -> bool:
        pass


class CreatePost(View):
    model = Post
    validator = PostValidate

    def get(self, request):
        return render(request, "create_post.html")

    def post(self, request):
        title = request.POST.get("title")
        content = request.POST.get("text")
        errors = []

        if not self.validator.is_valid(title, content):
            errors.append("Укажите заголовок и содержимое заметки")
            return render(request, "create_post.html", {"errors": errors})

        post = self.model(title=title, content=content)
        post.save()
        return redirect(reverse("post_show", kwargs={"post_id": post.id}))
