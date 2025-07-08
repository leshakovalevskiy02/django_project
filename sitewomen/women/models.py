from django.db import models
from django.urls import reverse
from django.template.defaultfilters import slugify
from taggit.managers import TaggableManager
from unidecode import unidecode
from django.core.validators import MinLengthValidator
from .validators import RussianValidator
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill
from django.contrib.auth import get_user_model


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
    photo = models.ImageField(upload_to="photos/%Y/%m/%d/", null=True, blank=True,
                              verbose_name="Фото")
    thumbnail = ImageSpecField(
        source='photo',
        processors=[ResizeToFill(300, 300)],
        format='JPEG',
        options={'quality': 80}
    )
    content = models.TextField(blank=True, verbose_name="Текст статьи")
    time_create = models.DateTimeField(auto_now_add=True, verbose_name="Время создания")
    time_update = models.DateTimeField(auto_now=True, verbose_name="Время изменения")
    is_published = models.IntegerField(default=Status.PUBLISHED, choices=Status.choices, verbose_name="Статус")
    cat = models.ForeignKey("Category", on_delete=models.PROTECT, related_name="posts",
                            related_query_name="where_posts", verbose_name="Категории")
    tags = models.ManyToManyField('TagPost', blank=True, related_name="tags", verbose_name="Тэги",
                                  related_query_name="tags")
    tags_taggle = TaggableManager()
    husband = models.OneToOneField("Husband", on_delete=models.SET_NULL, null=True, blank=True,
                                   related_name="woman", verbose_name="Муж")
    author = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL, related_name="posts", null=True)

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


class UploadFiles(models.Model):
    image = models.FileField(upload_to="uploads_model", verbose_name="Загрузить изображение")


class Comment(models.Model):
    post = models.ForeignKey(Women, on_delete=models.CASCADE, related_name='comments', verbose_name="Название поста")
    author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name="comments", verbose_name="Автор")
    parent = models.ForeignKey('self', on_delete=models.CASCADE,
                               null=True, blank=True, related_name='children')
    body = models.TextField(verbose_name="Комментарий")
    created = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")
    active = models.BooleanField(default=True, verbose_name="Статус")

    class Meta:
        verbose_name = "Коментарий"
        verbose_name_plural = "Коментарии"
        ordering = ['created']
        indexes = [
            models.Index(fields=['created']),
        ]

    def __str__(self):
        return f'Комментирует {self.author.username} пост {self.post}'