from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User
from datetime import datetime
from django.utils.safestring import mark_safe
from sitewomen import settings


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ("username", "email", "first_name", "last_name", "get_birthday", "get_photo")
    list_display_links = ("username", "email")

    @admin.display(description="Дата рождения")
    def get_birthday(self, user: User):
        if user.date_birth:
            return datetime.strftime(user.date_birth, "%d.%m.%Y")

    @admin.display(description="Фото")
    def get_photo(self, user):
        if user.photo:
            return mark_safe(f"<img src='{user.thumbnail.url}' width=50>")
        return mark_safe(f"<img src='{settings.DEFAULT_USER_IMAGE}' width=50>")
