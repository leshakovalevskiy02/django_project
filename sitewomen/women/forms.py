from django import forms
from .models import Category, Husband, TagPost

class AddPostForm(forms.Form):
    title = forms.CharField(max_length=255, label="Заголовок", widget=forms.TextInput(attrs={'class': 'form-input'}))
    slug = forms.SlugField(max_length=255, label="Слаг", disabled=True, required=False)
    content = forms.CharField(widget=forms.Textarea(attrs={"cols": 50, "rows": 5}), label="Текст статьи",
                              required=False)
    is_published = forms.BooleanField(label="Статус", required=False, initial=True)
    cat = forms.ModelChoiceField(label="Категория", queryset=Category.objects.all(), empty_label="Выберите категорию")
    husband = forms.ModelChoiceField(label="Муж", queryset=Husband.objects.all(), required=False, empty_label="Не замужем")
    tags = forms.ModelMultipleChoiceField(queryset=TagPost.objects.all(), required=False, label="Теги")


class ContactForm(forms.Form):
    name = forms.CharField(label="Ваше имя")
    email = forms.EmailField(label="Ваш email", widget=forms.EmailInput(attrs={"class": "form-label form-error"}),
                             initial="example@mail.ru")
    comment = forms.CharField(widget=forms.Textarea(attrs={"cols": "50", "rows": "5"}), label="Ваш комментарий")