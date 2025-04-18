from django.urls import path, re_path, register_converter
from . import views, converters

register_converter(converters.YearConverter, "year4")


urlpatterns = [
    path('', views.index, name="home"),  # http://127.0.0.1:8000
    path('about/', views.about, name="about"),  #  http://127.0.0.1:8000/about/
    path('cats/<int:cat_id>/', views.categories, name="cats_id"),  # http://127.0.0.1:8000/cats/3/
    path('cats/<slug:cat_slug>/', views.categories_by_slug, name="cats"),  # http://127.0.0.1:8000/cats/jenny/
    path("archive/<year4:year>/", views.archive, name="archive")  # http://127.0.0.1:8000/archive/2025/
]
