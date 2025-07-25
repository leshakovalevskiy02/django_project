from django.views.decorators.http import require_POST
from sitewomen import settings
from django.core.mail import EmailMessage
from django.http import HttpResponseNotFound
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.forms import ValidationError
from .models import Women, TagPost, Comment, Category
from .forms import AddPostForm, ContactForm, CommentForm, UpdatePostForm
from django.views.generic import ListView, DetailView, FormView, CreateView, UpdateView, DeleteView, TemplateView
from .utils import DataMixin, SearchFieldMixin
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.shortcuts import render, redirect, reverse
from django.db.models import Count
from django.contrib import messages


class HomePage(DataMixin, SearchFieldMixin, ListView):
    template_name = "women/index.html"
    context_object_name = 'posts'
    title = "Главная страница"
    extra_context = {
        "cat_selected":  0
    }
    paginate_by = 6

    def get_queryset(self):
        query = self.request.GET.get("query")
        queryset = Women.published.select_related("cat").select_related("author")
        return self.calculate_similarity(query, queryset)


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
        post_tags = post.tags.all()
        similar_posts = Women.published.filter(tags__in=post_tags).exclude(pk=post.id)
        similar_posts = similar_posts.annotate(same_tags=Count('tags')).order_by('-same_tags', '-time_update')[:4]
        context["title"] = post.title
        context["cat_selected"] = post.cat.pk
        context["comments"] = post.comments.filter(active=True, parent=None)
        context["form"] = CommentForm()
        context["similar_posts"] = similar_posts
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
    template_name = "women/edit_page.html"
    model = Women
    form_class = UpdatePostForm
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


class ShowCategory(DataMixin, SearchFieldMixin, ListView):
    template_name = "women/index.html"
    context_object_name = "posts"
    allow_empty = True

    def get_queryset(self):
        query = self.request.GET.get("query")
        cat_slug = self.kwargs["cat_slug"]
        queryset = Women.published.filter(cat__slug=cat_slug).select_related("cat").select_related("author")
        return self.calculate_similarity(query, queryset)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        category = Category.objects.get(slug=self.kwargs["cat_slug"])
        context["title"] = f"Рубрика: {category.name}"
        context["cat_selected"] = category.pk
        context["has_param"] = True
        context["param"] = category.slug
        return context


class ShowPostsBySlug(DataMixin, SearchFieldMixin, ListView):
    template_name = "women/index.html"
    context_object_name = "posts"

    def get_queryset(self):
        tag_slug = self.kwargs["tag_slug"]
        query = self.request.GET.get("query")
        queryset = Women.published.filter(tags__slug=tag_slug).select_related("cat").select_related("author")
        return self.calculate_similarity(query, queryset)

    def get_context_data(self, *, object_list=None, **kwargs):
        tag_slug = self.kwargs["tag_slug"]
        context = super().get_context_data(**kwargs)
        tag = get_object_or_404(klass=TagPost, slug=tag_slug)
        context["title"] = f"Тег - {tag.tag}"
        context["param"] = tag.slug
        return context


def page_not_found(request, exception):
    return HttpResponseNotFound("<h1>Страница не найдена</h1>")


@require_POST
def post_comment(request, post_id):
    post = get_object_or_404(Women, pk=post_id, is_published=Women.Status.PUBLISHED)
    comment = None
    form = CommentForm(data=request.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.post = post
        comment.author = request.user
        comment.save()
        messages.success(request, "Комментарий успешно добавлен.")
        url = reverse("post", args=(post.slug,))
        return redirect(url)
    return render(request, 'women/post/comment.html',{'post': post,
                                                      'form': form, "comment": comment})


def reply_comment(request, post_id, comment_id):
    comment_parent = get_object_or_404(Comment, pk=comment_id)
    post = get_object_or_404(Women, pk=post_id, is_published=Women.Status.PUBLISHED)

    if request.method == "GET":
        form = CommentForm()
    else:
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.parent = comment_parent
            comment.save()
            messages.success(request, "Ответ на комментарий успешно добавлен.")
            url = reverse("post", args=(post.slug,))
            return redirect(url)
    return render(request, "women/post/comment_reply.html",
                  {"comment": comment_parent, "post": post, "form": form})


def edit_comment(request, post_id, comment_id):
    comment = get_object_or_404(Comment, pk=comment_id)
    post = get_object_or_404(Women, pk=post_id, is_published=Women.Status.PUBLISHED)
    if request.method == "GET":
        form = CommentForm(instance=comment)
    else:
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            form.save()
            messages.success(request, "Комментарий успешно изменен.")
            url = reverse("post", args=(post.slug,))
            return redirect(url)
    return render(request, "women/post/comment_edit.html",
                  {"form": form, "post": post})