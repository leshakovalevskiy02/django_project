from captcha.fields import CaptchaField
from django import forms
from .models import Women, Comment


class AddPostForm(forms.ModelForm):
    is_published = forms.BooleanField(required=False, initial=True, label="Статус")

    class Meta:
        model = Women
        fields = ["title", "slug", "content", "photo", "is_published", "cat", "husband", "tags"]
        widgets = {
            "title": forms.TextInput(attrs={'class': 'form-input'}),
            "content": forms.Textarea(attrs={"cols": 50, "rows": 5}),
        }
        error_messages = {
            "title": {
                "required": "Без заголовка никак"
            }
        }


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["husband"].empty_label = "Не замужем"
        self.fields["cat"].empty_label = "Выберите категорию"


class ContactForm(forms.Form):
    name = forms.CharField(label="Ваше имя")
    email = forms.EmailField(label="Ваш email", widget=forms.EmailInput(attrs={"class": "form-label form-error"}),
                             initial="example@mail.ru")
    comment = forms.CharField(widget=forms.Textarea(attrs={"cols": "50", "rows": "5"}), label="Ваш комментарий")
    captcha = CaptchaField(label="Вы не робот?")


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["body"]

class SearchForm(forms.Form):
    query = forms.CharField(label="Введите поисковый запрос")