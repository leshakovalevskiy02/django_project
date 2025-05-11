from django import forms
from django.core.exceptions import ValidationError

from .models import Category, Husband, TagPost, Women
from unidecode import unidecode
from django.template.defaultfilters import slugify
from .validators import RussianValidator
import re


class AddPostForm(forms.Form):
    title = forms.CharField(max_length=255, min_length=5,
                            label="Заголовок", widget=forms.TextInput(attrs={'class': 'form-input'}),
                            error_messages={
                                "min_length": "Слишком короткий заголовок",
                                "required": "Без заголовка никак"
                            }, validators=[RussianValidator()])
    slug = forms.SlugField(max_length=255, label="Слаг", required=False, disabled=True)
    content = forms.CharField(widget=forms.Textarea(attrs={"cols": 50, "rows": 5}), label="Текст статьи",
                              required=False)
    is_published = forms.BooleanField(label="Статус", required=False, initial=True)
    cat = forms.ModelChoiceField(label="Категория", queryset=Category.objects.all(), empty_label="Выберите категорию")
    husband = forms.ModelChoiceField(label="Муж", queryset=Husband.objects.all(), required=False, empty_label="Не замужем")
    tags = forms.ModelMultipleChoiceField(queryset=TagPost.objects.all(), required=False, label="Теги")

    def clean(self):
        title = self.cleaned_data.get("title")

        if not title:
            return

        slug = slugify(unidecode(title))
        if Women.objects.filter(slug=slug).exists():
            raise ValidationError("Слаг должен быть уникальным. Измените заголовок записи")

        self.cleaned_data["slug"] = slug
        return self.cleaned_data


class ContactForm(forms.Form):
    name = forms.CharField(label="Ваше имя")
    email = forms.EmailField(label="Ваш email", widget=forms.EmailInput(attrs={"class": "form-label form-error"}),
                             initial="example@mail.ru")
    comment = forms.CharField(widget=forms.Textarea(attrs={"cols": "50", "rows": "5"}), label="Ваш комментарий")