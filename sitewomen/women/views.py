from django.http import HttpResponse, HttpResponseNotFound, Http404, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse

menu = [{'title': "О сайте", 'url_name': 'about'},
        {'title': "Добавить статью", 'url_name': 'add_page'},
        {'title': "Обратная связь", 'url_name': 'contact'},
        {'title': "Войти", 'url_name': 'login'}
]

data_db = [
    {'id': 1, 'title': 'Анджелина Джоли', 'content': '''<h1>Анджелина Джоли</h1> (англ. Angelina Jolie[7], при рождении Войт (англ. Voight), ранее Джоли Питт (англ. Jolie Pitt); род. 4 июня 1975, Лос-Анджелес, Калифорния, США) — американская актриса кино, телевидения и озвучивания, кинорежиссёр, сценаристка, продюсер, фотомодель, посол доброй воли ООН.
        Обладательница премии «Оскар», трёх премий «Золотой глобус» (первая актриса в истории, три года подряд выигравшая премию) и двух «Премий Гильдии киноактёров США».''',
     'is_published': True},
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
        "menu": menu,
    }
    return render(request, 'women/about.html', context=data)

def show_post(request, post_id):
    return HttpResponse(f"Отображение поста - {post_id}")

def addpage(request):
    return HttpResponse("Добавить статью")

def contact(request):
    return HttpResponse("Связаться с нами")

def login(request):
    return HttpResponse("Регистрация")

def page_not_found(request, exception):
    return HttpResponseNotFound("<h1>Страница не найдена</h1>")