from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DefaultUserAdmin
from django.utils.html import format_html

from .models import User
from .forms import UserRegisterForm


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    form = UserRegisterForm
    list_display = [
        "username",
        "email",
        "first_name",
        "last_name",
        "is_staff",
        "get_avatar_image",
    ]
    search_fields = ["username", ]

    @admin.display(description="Avatar")
    def get_avatar_image(self, obj: User):
        return format_html(
            f"""<img src={obj.avatar_image} height="80">"""  # должно быть {obj.avatar_image.url}, но не работает
        )
