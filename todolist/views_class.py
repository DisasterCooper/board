from django.shortcuts import render, redirect, get_object_or_404, reverse
from django.http import HttpResponseNotAllowed, Http404, HttpResponseForbidden
from django.urls import reverse_lazy
from django.views import View, generic
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.db.models import Count, Avg, Min, Max

from .models import Post, Comment


class PostsList(generic.View):

    @staticmethod
    def get_queryset():
        """
        Формирует 'QuerySet' всех заметок и возвращает поля id, title, created,
        имя пользователя, создавшего заметку и комментарии к ней.
        :return: Если values => возвращается 'QuerySet' словарей!
        """
        return Post.objects.all()\
            .select_related("user")\
            .annotate(Count("comments"))\
            .values("id", "title", "created", "user__username", "comments__count")\
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
        return render(request, "todolist/create_post.html")

    def post(self, request):
        validator = self.validator(title=request.POST.get("title", ""), content=request.POST.get("content", ""))

        if not validator.is_valid():
            return render(request, "todolist/create_post.html", {"validator": validator})

        post = self.model.objects.create(
            title=validator.title["value"],
            content=validator.content["value"],
            user=request.user
        )
        # post.save()
        return redirect(reverse("posts:show", kwargs={"post_id": post.id}))


@method_decorator(login_required, name="dispatch")
class EditPost(generic.View):
    model = Post
    validator = PostValidate

    def has_user_permission(self, post: Post) -> bool:
        return post.user.id == self.request.user.id

    def get(self, request, post_id: int):
        post = get_object_or_404(self.model, id=post_id)

        if not self.has_user_permission(post):
            return HttpResponseForbidden()

        validator = self.validator(post.title, post.content)
        return render(request, "todolist/edit_post.html", {"validator": validator})

    def post(self, request, post_id: int):
        post = get_object_or_404(self.model, id=post_id)

        validator = self.validator(title=request.POST.get("title", ""), content=request.POST.get("content", ""))
        post.title = validator.title["value"]
        post.content = validator.content["value"]
        if not validator.is_valid():
            return render(request, "todolist/edit_post.html", {"post": post})

        post.save()
        return redirect(reverse("posts:show", kwargs={"post_id": post_id}))


class ShowPost(generic.DetailView):
    queryset = Post.objects  # Откуда вытянуть
    pk_url_kwarg = "post_id"  # Где взять id объекта в URL?
    template_name = "todolist/show_post.html"  # Шаблон, куда вернуть
    context_object_name = "post"  # Под каким именем вернуть в этот шаблон


@method_decorator(login_required, name="dispatch")
class DeletePost(generic.View):
    model = Post
    queryset = Post.objects
    pk_url_kwarg = "post_id"
    success_url = reverse_lazy("home")

    def get_obj_pk(self):
        # для того чтобы из url '<int:post_id>/delete/' вытянуть значение, в данном случае post_id
        return self.kwargs[self.pk_url_kwarg]

    def get_queryset(self):
        return self.queryset

    def has_user_permission(self, post: Post) -> bool:
        return post.user.id == self.request.user.id

    def get_success_url(self):
        return self.success_url

    def post(self, request):
        qs = self.get_queryset()
        pk = self.get_obj_pk()
        try:
            obj_ = qs.get(id=pk)
        except self.model.DoesNotExist:
            raise Http404()

        if self.has_user_permission(obj_):
            obj_.delete()
            return redirect(self.get_success_url())

        else:
            return HttpResponseForbidden()

    # Проверку на ошибки используя try можно заменить, используя qs.filter для метода post.
    # Минус - заметка сразу удалится, без просмотра
    # qs.filter(pk=pk).delete()


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
