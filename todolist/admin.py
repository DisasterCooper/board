import textwrap

from django.contrib import admin

from .models import Post
# Tag добавить


@admin.register(Post)  # Модель
class PostAdmin(admin.ModelAdmin):  # Класс админки
    list_display = ["title",
                    "created",
                    "user",
                    "comments_count",
                    "tags_list"]

    @admin.display(description="Кол-во комментариев")
    def comments_count(self, obl: Post):
        return obl.comments_count

    @admin.display(description="Кол-во комментариев")
    def tags_list(self, obl: Post):
        return obl.tags.all().count()
    