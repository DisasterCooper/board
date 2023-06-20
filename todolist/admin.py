import textwrap

from django.contrib import admin
# from django.utils import format_html

from .models import Post
# Tag добавить можно еще


@admin.register(Post)  # Модель
class PostAdmin(admin.ModelAdmin):  # Класс админ панели
    list_display = ["_title",
                    "created",
                    "user",
                    "has_comments",
                    "comments_count",
                    # "tags_list"
                    ]
    search_fields = ["title", "content"]
    list_filter = ["user"]

    @admin.display(description="Title")
    def _title(self, obj: Post):
        return textwrap.wrap(obj.title, 25)[0] + "..."

    @admin.display(description="Comments", boolean=True)
    def has_comments(self, obj: Post):
        return obj.comments_count > 0

    @admin.display(description="Number of comments")
    def comments_count(self, obj: Post):
        return obj.comments_count

    # @admin.display(description="Tags")
    # def tags_list(self, obj: Post):
    #     return obj.tags.all().count()
