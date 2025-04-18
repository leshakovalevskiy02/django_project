from django.http import HttpResponse, HttpResponseNotFound, Http404, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.urls import reverse


def index(request):
    # t = render_to_string("women/index.html")
    # return HttpResponse(t)
    return render(request, "women/index.html")

def about(request):
    return render(request, 'women/about.html')

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