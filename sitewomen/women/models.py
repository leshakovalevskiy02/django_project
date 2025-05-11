from django.db import models
from django.urls import reverse
from django.template.defaultfilters import slugify
from taggit.managers import TaggableManager
from unidecode import unidecode
from django.core.validators import MinLengthValidator
from .validators import RussianValidator

class PublishedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_published=Women.Status.PUBLISHED)


class Women(models.Model):
    class Status(models.IntegerChoices):
        DRAFT = 0, "Черновик"
        PUBLISHED = 1, "Опубликовано"


    title = models.CharField(max_length=255, verbose_name="Заголовок",
                             validators=[
                                 MinLengthValidator(5, message="Слишком короткий заголовок"),
                                 RussianValidator()
                             ])
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name="Слаг", validators=[
                               MinLengthValidator(5, message="Минимум 5 символов")
                           ])
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

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(unidecode(self.title))
        super().save(*args, **kwargs)


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
        
    def save(self, *args, **kwargs):
        self.slug = slugify(unidecode(self.name))
        super().save(*args,  **kwargs)

class TagPost(models.Model):
    tag = models.CharField(max_length=100, db_index=True)
    slug = models.SlugField(max_length=255, unique=True, db_index=True)

    def __str__(self):
        return self.tag

    def get_absolute_url(self):
        return reverse("tag", args=(self.slug, ))
    
    def save(self, *args, **kwargs):
        self.slug = slugify(unidecode(self.tag))
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Тег"
        verbose_name_plural = "Теги"

class Husband(models.Model):
    name = models.CharField(max_length=100, verbose_name="Имя мужчины")
    age = models.IntegerField(null=True, verbose_name="Возраст")
    m_count = models.IntegerField(blank=True, default=0)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Мужчина"
        verbose_name_plural = "Мужчины"