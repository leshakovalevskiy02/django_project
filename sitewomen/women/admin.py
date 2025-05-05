from django.contrib import admin, messages
from .models import Women, Category, TagPost, Husband
from django.db.models.functions import Length
from django.db.models import Count, Q


class ContentFilter(admin.SimpleListFilter):
    title = "Сортировка по статьям"
    parameter_name = 'content'

    def lookups(self, request, model_admin):
        return [
            ("short", "Короткие статьи"),
            ("middle", "Средние статьи"),
            ("long", "Большие статьи")
        ]

    def queryset(self, request, queryset):
        queryset = queryset.annotate(length=Length("content"))
        if self.value() == "short":
            return queryset.filter(length__lt=800)
        if self.value() == "middle":
            return queryset.filter(length__range=(800, 1999))
        if self.value() == "long":
            return queryset.filter(length__gte=2000)


class MarriedFilter(admin.SimpleListFilter):
    parameter_name = "status"
    title = "Статус женщин"

    def lookups(self, request, model_admin):
        return [
            ("single", "Незамужняя"),
            ("married", "Замужем"),
        ]

    def queryset(self, request, queryset):
        if self.value() == "single":
            return queryset.filter(husband=None)
        if self.value() == "married":
            return queryset.filter(~Q(husband=None))

class AgeFilter(admin.SimpleListFilter):
    title = "Возрастные группы"
    parameter_name = "age_status"

    def lookups(self, request, model_admin):
        return [
            ("young", "Молодой возраст"),
            ("average", "Средний возраст"),
            ("elderly", "Пожилой возраст"),
            ("senile", "Старческий возраст"),
            ("longevity", "Долголетие")
        ]

    def queryset(self, request, queryset):
        if self.value() == "young":
            return queryset.filter(age__range=(18, 44))
        if self.value() == "average":
            return queryset.filter(age__range=(45, 59))
        if self.value() == "elderly":
            return queryset.filter(age__range=(60, 74))
        if self.value() == "senile":
            return queryset.filter(age__range=(75, 90))
        if self.value() == "longevity":
            return queryset.filter(age__gt=90)


@admin.register(Women)
class WomenAdmin(admin.ModelAdmin):
    # exclude = ("tags", "tags_taggle", "husband", "is_published")
    fields = ("title", "slug", "content", "cat", "husband", "tags")
    readonly_fields = ("slug", )
    # prepopulated_fields = {"slug": ("title", )}
    # filter_vertical = ("tags", )
    filter_horizontal = ("tags", )
    list_display = ("title", "time_create", "is_published", "cat", "brief_info")
    list_display_links = ("title", )
    ordering = ("-time_create", "title")
    list_editable = ("is_published", )
    list_per_page = 5
    actions = ("set_published", "set_draft")
    search_fields = ("title__startswith", "cat__name")
    list_filter = ("cat__name", "is_published", MarriedFilter, ContentFilter)

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
    list_display = ("name", "count_women_by_category")
    list_display_links = ("name", )
    search_fields = ("name", )
    readonly_fields = ("slug", )

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        queryset = queryset.annotate(nums=Count("where_posts",
                    filter=Q(where_posts__is_published=Women.Status.PUBLISHED))).filter(nums__gt=0)
        return queryset

    @admin.display(description="Количество женщин по категории", ordering="nums")
    def count_women_by_category(self, cat):
        return cat.nums

@admin.register(TagPost)
class TagsAdmin(admin.ModelAdmin):
    readonly_fields = ("slug", )
    search_fields = ("tag", )


@admin.register(Husband)
class HusbandAdmin(admin.ModelAdmin):
    fields = ("name", "age")
    list_display = ("name", "age")
    search_fields = ("name", )
    list_filter = (AgeFilter, )