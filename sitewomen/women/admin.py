from django.contrib import admin, messages
from django.db.models import Prefetch

from .models import Women, Category
from django.db.models.functions import Length
from django.db.models import Count, Q

@admin.register(Women)
class WomenAdmin(admin.ModelAdmin):
    list_display = ("title", "time_create", "is_published", "cat", "brief_info")
    list_display_links = ("title", )
    ordering = ("-time_create", "title")
    list_editable = ("is_published", )
    list_per_page = 5
    actions = ("set_published", "set_draft")

    @admin.display(description="Краткое описание", ordering=Length("content"))
    def brief_info(self, women: Women):
        return f"Описание {len(women.content)} символов."

    @admin.action(description="Опубликовать выбранные записи")
    def set_published(self, request, queryset):
        count = queryset.update(is_published=Women.Status.PUBLISHED)
        self.message_user(request, message=f"Было изменено {count} записей")

    @admin.action(description="Сделать выбранные записи черновиком")
    def set_draft(self, request, queryset):
        count = queryset.update(is_published=Women.Status.DRAFT)
        self.message_user(request, message=f"{count} записей снято с публикации", level=messages.WARNING)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "count_women_by_category")
    list_display_links = ("name", "id")

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        queryset = queryset.annotate(nums=Count("where_posts",
                    filter=Q(where_posts__is_published=Women.Status.PUBLISHED))).filter(nums__gt=0)
        return queryset

    @admin.display(description="Количество женщин по категории", ordering="nums")
    def count_women_by_category(self, cat):
        return cat.nums

# admin.site.register(Women, WomenAdmin)