from django.urls import path, register_converter
from . import views, converters
# from django.views.decorators.cache import cache_page


register_converter(converters.YearConverter, "year4")


urlpatterns = [
    path('', views.HomePage.as_view(), name="home"),
    path('about/', views.About.as_view(), name="about"),
    path('addpage/', views.AddPage.as_view(), name='add_page'),
    path('contact/', views.Contact.as_view(), name='contact'),
    path('post/<slug:post_slug>/', views.ShowPost.as_view(), name="post"),
    path('category/<slug:cat_slug>/', views.ShowCategory.as_view(), name='category'),
    path("tag/<slug:tag_slug>/", views.ShowPostsBySlug.as_view(), name="tag"),
    path("edit_post/<slug:slug>/", views.UpdatePage.as_view(), name="edit_post"),
    path("delete_post/<slug:slug>/", views.DeletePage.as_view(), name="delete_post"),
    path('comment/<int:post_id>/', views.post_comment, name='post_comment'),
    path('reply_comment/<int:post_id>/<int:comment_id>/', views.reply_comment, name='reply_comment'),
    path('edit_comment/<int:post_id>/<int:comment_id>/', views.edit_comment, name='edit_comment'),
]
