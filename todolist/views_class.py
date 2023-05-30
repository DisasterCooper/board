from django.shortcuts import render, redirect, get_object_or_404, reverse
from django.http import HttpResponseNotAllowed, Http404
from django.urls import reverse_lazy
from django.views import View, generic

from .models import Post


class PostsList(View):

    @staticmethod
    def get_queryset():
        return Post.objects.all()

    def get(self, request):
        posts = self.get_queryset()  # QuerySet все заметки
        return render(request, "todolist/home.html", {"posts": posts})


class PostValidate:

    def __init__(self, title: str, content: str):
        self.title = title
        self.content = content

    @classmethod
    def is_valid(cls, title: str, content: str) -> bool:
        return cls.validate_title(title) and cls.validate_content(content)

    @staticmethod
    def validate_title(title: str) -> bool:
        return len(title) <= 100

    @staticmethod
    def validate_content(content: str) -> bool:
        return len(content) <= 1000


class CreatePost(View):
    model = Post
    validator = PostValidate

    def get(self, request):
        return render(request, "todolist/create_post.html")

    def post(self, request):
        title = request.POST.get("title")
        content = request.POST.get("content")
        errors = []

        if not self.validator.is_valid(title, content):
            errors.append("Укажите заголовок и содержимое заметки")
            return render(request, "todolist/create_post.html", {"errors": errors})

        post = self.model(title=title, content=content)
        post.save()
        return redirect(reverse("post_show", kwargs={"post_id": post.id}))


class ShowPost(generic.DetailView):
    queryset = Post.objects  # Откуда вытянуть
    pk_url_kwarg = "post_id"  # Где взять id объекта в URL?
    template_name = "todolist/show_post.html"  # Шаблон, куда вернуть
    context_object_name = "post"  # Под каким именем вернуть в этот шаблон


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

    def get_success_url(self):
        return self.success_url

    def post(self, request):
        qs = self.get_queryset()
        pk = self.get_obj_pk()
        try:
            obj_ = qs.get(id=pk)
        except self.model.DoesNotExist:
            raise Http404()
        else:
            obj_.delete()
            return redirect(self.get_success_url())
