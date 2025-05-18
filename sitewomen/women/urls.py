from django.urls import path, re_path, register_converter
from . import views, converters

register_converter(converters.YearConverter, "year4")


urlpatterns = [
    path('', views.HomePage.as_view(), name="home"),  # http://127.0.0.1:8000
    path('about/', views.about, name="about"),  #  http://127.0.0.1:8000/about/
    path('addpage/', views.AddPage.as_view(), name='add_page'),
    path('contact/', views.contact, name='contact'),
    path('login/', views.login, name='login'),
    path('post/<slug:post_slug>/', views.ShowPost.as_view(), name="post"),
    path('category/<slug:cat_slug>/', views.ShowCategory.as_view(), name='category'),
    path("tag/<slug:tag_slug>/", views.ShowPostsBySlug.as_view(), name="tag")
]
