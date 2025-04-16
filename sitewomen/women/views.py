from django.http import HttpResponse
from django.shortcuts import render

def index(request):
    return HttpResponse("Страница приложения women")

def categories(request, cat_id):
    return HttpResponse(f"Категория {cat_id} <h1> blabla </h1>")

def categories_by_slug(request, cat_slug):
    return HttpResponse(f"{cat_slug} категория")

def archive(request, year):
    return HttpResponse(f"Архив по годам - {year}")