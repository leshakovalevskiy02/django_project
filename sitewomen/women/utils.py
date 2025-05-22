from django.views.generic.base import ContextMixin

menu = [{'title': "О сайте", 'url_name': 'about'},
        {'title': "Добавить статью", 'url_name': 'add_page'},
        {'title': "Обратная связь", 'url_name': 'contact'},
        {'title': "Войти", 'url_name': 'login'}
]


class DataMixin(ContextMixin):
    extra_context = {}
    title = None

    def __init__(self):
        if self.title is not None:
            self.extra_context["title"] = self.title

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["menu"] = menu
        if "cat_selected" not in context:
            context["cat_selected"] = None
        return context