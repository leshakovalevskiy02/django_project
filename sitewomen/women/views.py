from django.http import HttpResponse, HttpResponseNotFound, Http404, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from women.templatetags.custom_filters import add_email_to_string

menu = ["О сайте", "Добавить статью", "Обратная связь", "Войти"]

data_db = [
    {'id': 1, 'title': 'Анджелина Джоли', 'content': 'Биография Анджелины Джоли', 'is_published': True},
    {'id': 2, 'title': 'Марго Робби', 'content': 'Биография Марго Робби', 'is_published': False},
    {'id': 3, 'title': 'Джулия Робертс', 'content': 'Биография Джулия Робертс', 'is_published': True},
]


def index(request):
    data = {
        "title": "Главная страница",
        "menu": menu,
        "posts": [post for post in data_db if post["is_published"]]
    }
    return render(request, "women/index.html", context=data)

def about(request):
    data = {
        "title": "О сайте",
        "mail": add_email_to_string("my_site", "gmail.com")
    }
    return render(request, 'women/about.html', context=data)

def categories(request, cat_id):
    return HttpResponse(f"Категория {cat_id} <h1> blabla </h1>")

def categories_by_slug(request, cat_slug):
    if request.GET:
        data = [f"{key}={item}" for key, value in request.GET.lists() for item in value]
        return HttpResponse(f'Переданные параметры - {"|".join(data)}<p>{cat_slug} категория</p>')
    return HttpResponse(f"{cat_slug} категория")

def archive(request, year):
    if year > 2023:
        uri = reverse('cats', args=('music', ))
        return HttpResponseRedirect(uri)

    return HttpResponse(f"Архив по годам - {year}")

def page_not_found(request, exception):
    return HttpResponseNotFound("<h1>Страница не найдена</h1>")