from django.db import models
from django.urls import reverse
from taggit.managers import TaggableManager


class PublishedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_published=Women.Status.PUBLISHED)


class Women(models.Model):
    class Status(models.IntegerChoices):
        DRAFT = 0, "Черновик"
        PUBLISHED = 1, "Опубликовано"


    title = models.CharField(max_length=255, verbose_name="Заголовок")
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name="Слаг")
    content = models.TextField(blank=True, verbose_name="Текст статьи")
    time_create = models.DateTimeField(auto_now_add=True, verbose_name="Время создания")
    time_update = models.DateTimeField(auto_now=True, verbose_name="Время изменения")
    is_published = models.IntegerField(default=Status.PUBLISHED, choices=Status.choices, verbose_name="Статус")
    cat = models.ForeignKey("Category", on_delete=models.PROTECT, related_name="posts",
                            related_query_name="where_posts", verbose_name="Категории")
    tags = models.ManyToManyField('TagPost', blank=True, related_name="tags", verbose_name="Тэги")
    tags_taggle = TaggableManager()
    husband = models.OneToOneField("Husband", on_delete=models.SET_NULL, null=True, blank=True,
                                   related_name="woman", verbose_name="Муж")

    objects = models.Manager()
    published = PublishedManager()

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Известные женщины"
        verbose_name_plural = "Известные женщины"
        ordering = ["-time_create"]
        get_latest_by = ["time_create"]
        indexes = [
            models.Index(fields=["-time_create"])
        ]

    def get_absolute_url(self):
        return reverse("post", args=(self.slug, ))


class Category(models.Model):
    name = models.CharField(max_length=100, db_index=True, verbose_name="Категория")
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name="Слаг")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("category", args=(self.slug,))

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

class TagPost(models.Model):
    tag = models.CharField(max_length=100, db_index=True)
    slug = models.SlugField(max_length=255, unique=True, db_index=True)

    def __str__(self):
        return self.tag

    def get_absolute_url(self):
        return reverse("tag", args=(self.slug, ))

class Husband(models.Model):
    name = models.CharField(max_length=100)
    age = models.IntegerField(null=True)
    m_count = models.IntegerField(blank=True, default=0)

    def __str__(self):
        return self.name