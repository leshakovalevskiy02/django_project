from sitewomen import settings
from django.core.mail import EmailMessage
from django.http import HttpResponseNotFound
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.forms import ValidationError
from .models import Women, TagPost
from .forms import AddPostForm, ContactForm
from django.views.generic import ListView, DetailView, FormView, CreateView, UpdateView, DeleteView, TemplateView
from .utils import DataMixin
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.core.cache import cache


class HomePage(DataMixin, ListView):
    template_name = "women/index.html"
    context_object_name = 'posts'
    title = "Главная страница"
    extra_context = {
        "cat_selected":  0
    }

    def get_queryset(self):
        value = cache.get("women_list")
        if value is None:
            value = Women.published.select_related("cat").select_related("author")
            cache.set("women_list", value, timeout=60)

        return value


class About(LoginRequiredMixin, DataMixin, TemplateView):
    template_name = 'women/about.html'
    title = "О сайте"


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


class AddPage(PermissionRequiredMixin, DataMixin, CreateView):
    permission_required = "women.add_women"
    template_name = "women/addpage.html"
    form_class = AddPostForm
    success_url = reverse_lazy("home")
    title = "Добавить статью"

    def form_valid(self, form):
        w = form.save(commit=False)
        w.author = self.request.user
        return super().form_valid(form)


class UpdatePage(PermissionRequiredMixin, DataMixin, UpdateView):
    permission_required = "women.change_women"
    template_name = "women/addpage.html"
    model = Women
    fields = ["title", "content", "photo", "is_published", "cat"]
    success_url = reverse_lazy("home")
    title = "Редактирование статьи"


class DeletePage(PermissionRequiredMixin, DataMixin, DeleteView):
    permission_required = "women.delete_women"
    template_name = "women/delete_post.html"
    success_url = reverse_lazy("home")
    context_object_name = "post"
    model = Women
    title = "Удаление статьи"


class Contact(LoginRequiredMixin, DataMixin, FormView):
    form_class = ContactForm
    template_name = "women/contact.html"
    title = "Форма для обратной связи"
    success_url = reverse_lazy("home")

    def form_valid(self, form):
        cd = form.cleaned_data
        user = self.request.user
        try:
            if user.email != cd["email"]:
                raise ValidationError(message="Это не ваш E-mail адрес")
            EmailMessage(
                f'Сообщение от {cd["name"]}',
                f"Вопрос пользователя - {cd['comment']}",
                from_email=settings.DEFAULT_FROM_EMAIL,
                to=[settings.DEFAULT_FROM_EMAIL],
                reply_to=[cd["email"]]
            ).send()
            return super().form_valid(form)
        except ValidationError as e:
            form.add_error("email", e.message)
            return self.form_invalid(form)


class ShowCategory(DataMixin, ListView):
    template_name = "women/index.html"
    context_object_name = "posts"
    allow_empty = False

    def get_queryset(self):
        cat_slug = self.kwargs["cat_slug"]
        return Women.published.filter(cat__slug=cat_slug).select_related("cat").select_related("author")

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