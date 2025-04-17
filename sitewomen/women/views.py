from django.http import HttpResponse, HttpResponseNotFound, Http404
from django.shortcuts import render

def index(request):
    return HttpResponse("Страница приложения women")

def categories(request, cat_id):
    return HttpResponse(f"Категория {cat_id} <h1> blabla </h1>")

def categories_by_slug(request, cat_slug):
    if request.GET:
        print(request.GET)
    return HttpResponse(f"{cat_slug} категория")

def archive(request, year):
    if year > 2023:
        raise Http404()

    return HttpResponse(f"Архив по годам - {year}")

def page_not_found(request, exception):
    return HttpResponseNotFound("<h1>Страница не найдена</h1>")