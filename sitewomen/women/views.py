from django.http import HttpResponse, HttpResponseNotFound, Http404, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from .models import Women, Category, TagPost
from .forms import AddPostForm, ContactForm, UploadFilesForm
import uuid
from os.path import splitext
from django.views import View
from django.views.generic import TemplateView, ListView, DetailView

menu = [{'title': "О сайте", 'url_name': 'about'},
        {'title': "Добавить статью", 'url_name': 'add_page'},
        {'title': "Обратная связь", 'url_name': 'contact'},
        {'title': "Войти", 'url_name': 'login'}
]


class HomePage(ListView):
    # model = Women
    template_name = "women/index.html"
    # template_name_suffix = ""
    context_object_name = 'posts'
    queryset = Women.published.select_related("cat")
    extra_context = {
            "title": "Главная страница",
            "menu": menu,
            "cat_selected": 0,
        }

    # def get_queryset(self):
    #     return Women.published.select_related("cat")


# def index(request):
#     data = {
#         "title": "Главная страница",
#         "menu": menu,
#         "posts": Women.published.select_related("cat"),
#         "cat_selected": 0,
#     }
#     return render(request, "women/index.html", context=data)

def handle_uploaded_file(f):
    file_name, file_extension = splitext(f.name)
    pk = str(uuid.uuid4())
    unique_name = file_name + pk + file_extension
    with open(f"files/{unique_name}", "wb+") as destination:
        for chunk in f.chunks():
            destination.write(chunk)

def about(request):
    if request.method == "POST":
        form = UploadFilesForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
    else:
        form = UploadFilesForm()

    data = {
        "title": "О сайте",
        "menu": menu,
        "form": form
    }
    return render(request, 'women/about.html', context=data)

# def show_post(request, post_slug):
#     post = get_object_or_404(klass=Women, slug=post_slug)
#     data = {
#         'title': post.title,
#         'menu': menu,
#         'post': post,
#         'cat_selected': post.cat.pk,
#     }
#     return render(request, "women/post.html", context=data)


class ShowPost(DetailView):
    template_name = "women/post.html"
    context_object_name = "post"
    slug_url_kwarg = "post_slug"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post = context["post"]
        context["title"] = post.title
        context["menu"] = menu
        context['cat_selected'] = post.cat.pk
        return context

    def get_object(self, queryset=None):
        slug = self.kwargs[self.slug_url_kwarg]
        return get_object_or_404(Women.published, slug=slug)

# def addpage(request):
#     if request.method == "POST":
#         form = AddPostForm(request.POST, request.FILES)
#         if form.is_valid():
#             form.save()
#             return redirect("home")
#     else:
#         form = AddPostForm()
#     data = {
#         'title': "Добавление статьи",
#         'menu': menu,
#         "form": form
#     }
#     return render(request, "women/addpage.html", context=data)


class AddPage(View):
    def get(self, request):
        form = AddPostForm()
        data = {
            'title': "Добавление статьи",
            'menu': menu,
            "form": form
        }
        return render(request, "women/addpage.html", context=data)

    def post(self, request):
        form = AddPostForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect("home")
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

# def show_category(request, cat_slug):
#     category = get_object_or_404(klass=Category, slug=cat_slug)
#     data = {
#         "title": f"Рубрика: {category.name}",
#         "menu": menu,
#         "posts": Women.published.filter(cat__slug=cat_slug).select_related("cat"),
#         "cat_selected": category.pk,
#     }
#     return render(request, "women/index.html", context=data)

class ShowCategory(ListView):
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
        context["menu"] = menu
        context["cat_selected"] = category.pk
        return context


def page_not_found(request, exception):
    return HttpResponseNotFound("<h1>Страница не найдена</h1>")


# def show_posts_by_tag(request, tag_slug):
#     tag = get_object_or_404(klass=TagPost, slug=tag_slug)
#     data = {
#         "title": f"Тег - {tag.tag}",
#         "menu": menu,
#         "posts": Women.published.filter(tags__slug=tag_slug).select_related("cat"),
#         "cat_selected": None,
#     }
#     return render(request, "women/index.html", context=data)

class ShowPostsBySlug(ListView):
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
        context["menu"] = menu
        context["cat_selected"] = None
        return context