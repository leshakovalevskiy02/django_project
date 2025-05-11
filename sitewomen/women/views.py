from django.http import HttpResponse, HttpResponseNotFound, Http404, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from .models import Women, Category, TagPost
from .forms import AddPostForm, ContactForm
from django.db.models.query import QuerySet

menu = [{'title': "О сайте", 'url_name': 'about'},
        {'title': "Добавить статью", 'url_name': 'add_page'},
        {'title': "Обратная связь", 'url_name': 'contact'},
        {'title': "Войти", 'url_name': 'login'}
]


def index(request):
    data = {
        "title": "Главная страница",
        "menu": menu,
        "posts": Women.published.select_related("cat"),
        "cat_selected": 0,
    }
    return render(request, "women/index.html", context=data)

def about(request):
    data = {
        "title": "О сайте",
        "menu": menu,
    }
    return render(request, 'women/about.html', context=data)

def show_post(request, post_slug):
    post = get_object_or_404(klass=Women, slug=post_slug)
    data = {
        'title': post.title,
        'menu': menu,
        'post': post,
        'cat_selected': post.cat.pk,
    }
    return render(request, "women/post.html", context=data)

def addpage(request):
    if request.method == "POST":
        form = AddPostForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("home")
    else:
        form = AddPostForm()
    data = {
        'title': "Добавление статьи",
        'menu': menu,
        "form": form
    }
    return render(request, "women/addpage.html", context=data)

def contact(request):
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            print(form.cleaned_data)
            return redirect("home")
    else:
        form = ContactForm()
    data = {
        'title': "Форма для обратной связи",
        'menu': menu,
        "form": form
    }
    return render(request, "women/contact.html", context=data)

def login(request):
    return HttpResponse("Регистрация")

def show_category(request, cat_slug):
    category = get_object_or_404(klass=Category, slug=cat_slug)
    data = {
        "title": f"Рубрика: {category.name}",
        "menu": menu,
        "posts": Women.published.filter(cat__slug=cat_slug).select_related("cat"),
        "cat_selected": category.pk,
    }
    return render(request, "women/index.html", context=data)


def page_not_found(request, exception):
    return HttpResponseNotFound("<h1>Страница не найдена</h1>")


def show_posts_by_tag(request, tag_slug):
    tag = get_object_or_404(klass=TagPost, slug=tag_slug)
    data = {
        "title": f"Тег - {tag.tag}",
        "menu": menu,
        "posts": Women.published.filter(tags__slug=tag_slug).select_related("cat"),
        "cat_selected": None,
    }
    return render(request, "women/index.html", context=data)