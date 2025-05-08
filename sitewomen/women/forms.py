from django import forms
from .models import Category, Husband, TagPost

class AddPostForm(forms.Form):
    title = forms.CharField(max_length=255, label="Заголовок")
    slug = forms.SlugField(max_length=255, label="Слаг")
    content = forms.CharField(widget=forms.Textarea, label="Текст статьи", required=False)
    is_published = forms.BooleanField(label="Опубликовано", required=False)
    cat = forms.ModelChoiceField(label="Категория", queryset=Category.objects.all(), empty_label="Выберите категорию")
    husband = forms.ModelChoiceField(label="Муж", queryset=Husband.objects.all(), required=False)
    tags = forms.ModelMultipleChoiceField(queryset=TagPost.objects.all(), required=False)