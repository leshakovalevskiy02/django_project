from captcha.fields import CaptchaField
from django import forms
from .models import Women, Comment


class AddPostForm(forms.ModelForm):
    is_published = forms.BooleanField(required=False, initial=True, label="Статус",
                        widget=forms.CheckboxInput(attrs={"class": "form-check-input px-0"}))

    class Meta:
        model = Women
        fields = ["title", "slug", "content", "photo", "is_published", "cat", "husband", "tags"]
        widgets = {
            "title": forms.TextInput(attrs={'class': 'form-control w-25'}),
            "slug": forms.TextInput(attrs={"class": 'form-control w-25'}),
            "content": forms.Textarea(attrs={"class": 'form-control w-50', "rows": 5}),
            "photo": forms.ClearableFileInput(attrs={"class": "form-control w-50"}),
            "cat": forms.Select(attrs={"class": "form-select form-select-sm w-25"}),
            "husband": forms.Select(attrs={"class": "form-select form-select-sm w-25"}),
            "tags": forms.SelectMultiple(attrs={"class": "form-select w-25"})
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


class UpdatePostForm(forms.ModelForm):
    is_published = forms.BooleanField(required=False, initial=True, label="Статус",
                                      widget=forms.CheckboxInput(attrs={"class": "form-check-input px-0"}))

    class Meta:
        model = Women
        fields = ["title", "content", "photo", "is_published", "cat"]
        widgets = {
            "title": forms.TextInput(attrs={'class': 'form-control w-25'}),
            "content": forms.Textarea(attrs={"class": 'form-control w-50', "rows": 5}),
            "photo": forms.ClearableFileInput(attrs={"class": "form-control w-50"}),
            "cat": forms.Select(attrs={"class": "form-select form-select-sm w-25"})
        }
        error_messages = {
            "title": {
                "required": "Без заголовка никак"
            }
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["cat"].empty_label = "Выберите категорию"


class ContactForm(forms.Form):
    name = forms.CharField(label="Ваше имя", widget=forms.TextInput(attrs={"class": "form-control w-25"}))
    email = forms.EmailField(label="Ваш email", widget=forms.EmailInput(attrs={"class": "form-control w-25"}),
                             initial="example@mail.ru")
    comment = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control w-50', "rows": 5}),
                              label="Ваш комментарий")
    captcha = CaptchaField(label="Вы не робот?")


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["body"]
        widgets = {
            "body": forms.Textarea(attrs={'class': 'col col-4 is-invalid', "rows":5,
                                          "placeholder": "Введите ваш комментарий"})
        }


class SearchForm(forms.Form):
    query = forms.CharField(label="Введите поисковый запрос",
                    widget=forms.TextInput(attrs={"class": "form-control me-2", "placeholder": "Поиск..."}))