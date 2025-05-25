from django.core.paginator import Paginator
from django.http import HttpResponse, HttpResponseNotFound
from django.shortcuts import redirect, get_object_or_404, render
from django.urls import reverse, reverse_lazy
from .models import Women, TagPost
from .forms import AddPostForm, ContactForm
from django.views.generic import ListView, DetailView, FormView, CreateView, UpdateView, DeleteView, TemplateView
from .utils import DataMixin
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

class HomePage(DataMixin, ListView):
    template_name = "women/index.html"
    context_object_name = 'posts'
    queryset = Women.published.select_related("cat")
    title = "Главная страница"
    extra_context = {
        "cat_selected":  0
    }

# @login_required(login_url="users:login")
# def about(request):
#     return render(request, 'women/about.html', {"title": "О сайте"})

class About(LoginRequiredMixin, DataMixin, TemplateView):
    template_name = 'women/about.html'
    title = "О сайте"
    # login_url = "users:login"


class ShowPost(DataMixin, DetailView):
    template_name = "women/post.html"
    context_object_name = "post"
    slug_url_kwarg = "post_slug"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post = context["post"]
        context["title"] = post.title
        context["cat_selected"] = post.cat.pk
        return context

    def get_object(self, queryset=None):
        slug = self.kwargs[self.slug_url_kwarg]
        return get_object_or_404(Women.published, slug=slug)


class AddPage(LoginRequiredMixin, DataMixin, CreateView):
    template_name = "women/addpage.html"
    form_class = AddPostForm
    success_url = reverse_lazy("home")
    title = "Добавить статью"

    def form_valid(self, form):
        w = form.save(commit=False)
        w.author = self.request.user
        return super().form_valid(form)


class UpdatePage(LoginRequiredMixin, DataMixin, UpdateView):
    template_name = "women/addpage.html"
    model = Women
    fields = ["title", "content", "photo", "is_published", "cat"]
    success_url = reverse_lazy("home")
    title = "Редактирование статьи"


class DeletePage(LoginRequiredMixin, DataMixin, DeleteView):
    template_name = "women/delete_post.html"
    success_url = reverse_lazy("home")
    context_object_name = "post"
    model = Women
    title = "Удаление статьи"


class Contact(DataMixin, FormView):
    form_class = ContactForm
    template_name = "women/contact.html"
    title = "Форма для обратной связи"

    def form_valid(self, form):
        print(form.cleaned_data)
        return redirect("home")


class ShowCategory(DataMixin, ListView):
    template_name = "women/index.html"
    context_object_name = "posts"
    allow_empty = False

    def get_queryset(self):
        cat_slug = self.kwargs["cat_slug"]
        return Women.published.filter(cat__slug=cat_slug).select_related("cat")

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        category = context["posts"][0].cat
        context["title"] = f"Рубрика: {category.name}"
        context["cat_selected"] = category.pk
        return context


class ShowPostsBySlug(DataMixin, ListView):
    template_name = "women/index.html"
    context_object_name = "posts"

    def get_queryset(self):
        tag_slug = self.kwargs["tag_slug"]
        return Women.published.filter(tags__slug=tag_slug).select_related("cat")

    def get_context_data(self, *, object_list=None, **kwargs):
        tag_slug = self.kwargs["tag_slug"]
        context = super().get_context_data(**kwargs)
        tag = get_object_or_404(klass=TagPost, slug=tag_slug)
        context["title"] = f"Тег - {tag.tag}"
        return context


def page_not_found(request, exception):
    return HttpResponseNotFound("<h1>Страница не найдена</h1>")