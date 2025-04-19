from django.http import HttpResponse, HttpResponseNotFound, Http404, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.urls import reverse

menu = ["О сайте", "Добавить статью", "Обратная связь", "Войти"]

class MyClass:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def show_coords(self):
        return f"Координата точки - {self.x, self.y}"


def index(request):
    # t = render_to_string("women/index.html")
    # return HttpResponse(t)
    data = {
        "title": "Главная страница",
        "menu": menu,
        "float": 10.8,
        "tpl": (1, 2, "abc", True),
        "set": {1, 2, 3, 4, 5},
        "dict": {"key_1": "value_1", "key_2": "value_2"},
        "obj": MyClass(10, 20)
    }
    return render(request, "women/index.html", context=data)

def about(request):
    return render(request, 'women/about.html', context={"title": "О сайте"})

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