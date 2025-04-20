from django.urls import path, re_path, register_converter
from . import views, converters

register_converter(converters.YearConverter, "year4")


urlpatterns = [
    path('', views.index, name="home"),  # http://127.0.0.1:8000
    path('about/', views.about, name="about"),  #  http://127.0.0.1:8000/about/
    path('addpage/', views.addpage, name='add_page'),
    path('contact/', views.contact, name='contact'),
    path('login/', views.login, name='login'),
    path('post/<int:post_id>/', views.show_post, name="post"),
]
