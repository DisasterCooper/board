from datetime import datetime, timedelta

from django.db import transaction
from django.shortcuts import render, redirect, get_object_or_404, reverse
from django.http import HttpResponseNotAllowed, Http404, HttpResponseForbidden
from django.urls import reverse_lazy
from django.views import View, generic
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.db.models import Count, Avg, Min, Max

from .models import Post, Comment
from .forms import PostForm
from user.models import User as usermodel


class PostsList(generic.View):

    @staticmethod
    def get_queryset():
        """
        Формирует 'QuerySet' всех заметок и возвращает поля id, title, created,
        имя пользователя, создавшего заметку и количество комментариев к этой заметке.
        :return: Если values => возвращается 'QuerySet' словарей!
        """
        return Post.objects.all() \
            .select_related("user") \
            .annotate(Count("comments")) \
            .values("id", "title", "created", "user__username", "comments__count") \
            .order_by("-comments__count")

    def get(self, request):
        """
        Отображение всех заметок на главной странице.
        :param request: Обязательный, всегда, первый, запрос от пользователя.
        :return:
        """
        posts = self.get_queryset()  # QuerySet все заметки
        return render(request, "todolist/home.html", {"posts": posts})


class PostValidate:

    def __init__(self, title: str, content: str):
        self.title = {
            "value": title,
            "errors": [],
            "is_valid": True
        }
        self.content = {
            "value": content,
            "errors": [],
            "is_valid": True
        }

    # @classmethod
    def is_valid(self) -> bool:
        if not self.validate_title():
            self.title["is_valid"] = False
        if not self.validate_content():
            self.content["is_valid"] = False

        return self.title["is_valid"] and self.content["is_valid"]

    # @staticmethod
    def validate_title(self) -> bool:
        self.title["value"] = self.title["value"].strip()

        if not self.title["value"]:
            self.title["errors"].append("Add a title")
            return False

        len_title = 50
        if len(self.title["value"]) > len_title:
            self.title["errors"].append(f"The title can have only {len_title} characters")
            return False
        return True

    # @staticmethod
    def validate_content(self) -> bool:
        self.content["value"] = self.content["value"].strip()

        if not self.content["value"]:
            self.content["errors"].append("Add a content")
            return False

        len_content = 500
        if len(self.content["value"]) > len_content:
            self.content["errors"].append(f"The content can have only {len_content} characters")
            return False
        return True


@method_decorator(login_required, name="dispatch")
class CreatePost(generic.View):
    model = Post
    validator = PostValidate

    def get(self, request):
        form = PostForm(initial={"title": "Add title here"})
        return render(request, "todolist/create_post.html", {"form": form})

    def post(self, request):
        form = PostForm(request.POST)  # Create form for users data

        if not form.is_valid():  # Проверка данных пользователя
            return render(request, "todolist/create_post.html", {"form": form})

        with transaction.atomic():
            # После валидации обязательно получаем очищенные данные
            title = form.cleaned_data["title"]
            content = form.cleaned_data["content"]

            post = self.model.objects.create(
                title=title,
                content=content,
                user=request.user
            )
            post.save()
        return redirect(reverse("posts:show", kwargs={"post_id": post.id}))


@method_decorator(login_required, name="dispatch")
class EditPost(generic.UpdateView):
    model = Post
    form_class = PostForm
    pk_url_kwarg = "post_id"
    template_name = "todolist/edit_post.html"


class ShowPost(generic.DetailView):
    queryset = Post.objects  # Откуда вытянуть
    pk_url_kwarg = "post_id"  # Где взять id объекта в URL?
    template_name = "todolist/show_post.html"  # Шаблон, куда вернуть
    context_object_name = "post"  # Под каким именем вернуть в этот шаблон
    image = "img/img.png"  # !! Добавить для TODOLIST фоновую картинку (или удалить строку эту)


@method_decorator(login_required, name="dispatch")
class DeletePost(generic.DeleteView):
    model = Post
    queryset = Post.objects
    pk_url_kwarg = "post_id"
    success_url = reverse_lazy("posts:home")
    template_name = "todolist/delete_post.html"

    def form_valid(self, form):
        if self.object.user != self.request.user:
            return HttpResponseForbidden()
        return super().form_valid(form)


class CommentAdd(generic.View):

    def post(self, request, post_id: int):
        post = get_object_or_404(Post, id=post_id)

        user = request.POST.get("user", "")
        email = request.POST.get("email", "")
        content = request.POST.get("content", "")

        Comment.objects.create(
            username=user,
            email=email,
            content=content,
            post=post,
        )
        return redirect(reverse("posts:show", kwargs={"post_id": post.id}))


class ProfileUsers(generic.View):

    @staticmethod
    def get_queryset():
        return Post.objects.all() \
            .select_related("user") \
            .annotate(
                comments__count=Count("comments", distinct=True),
                comments__created=Max("comments__created"),
                )\
            .values("id", "title", "created", "user__username", "comments__count", "comments__created") \
            .order_by("-comments__count")

    def get(self, request):
        posts = self.get_queryset()
        return render(request, "todolist/profile_users.html", {"posts": posts})


class TopPosts(generic.View):

    @staticmethod
    def get_queryset():
        return Post.objects.all() \
            .select_related("user", "todolist_comment") \
            .filter(comments__created__gte=(datetime.now() - timedelta(hours=12))) \
            .annotate(
                comments__count=Count("comments", distinct=True),
                ) \
            .values("id", "title", "created", "user__username", "comments__count") \
            .order_by("-comments__count")

    def get(self, request):
        posts = self.get_queryset()
        return render(request, "todolist/top_posts.html", {"posts": posts})
