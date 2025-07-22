from django.views.generic.base import ContextMixin
from .forms import SearchForm
from django.contrib.postgres.search import TrigramSimilarity, TrigramWordSimilarity
from django.urls import resolve


class DataMixin(ContextMixin):
    extra_context = {}
    title = None
    paginate_by = 3

    def __init__(self):
        if self.title is not None:
            self.extra_context["title"] = self.title

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if "cat_selected" not in context:
            context["cat_selected"] = None
        if "paginator" in context:
            context["elided_page_range"] = context["paginator"].get_elided_page_range(
                        context["page_obj"].number, on_each_side=2, on_ends=1)
        return context


class SearchFieldMixin(ContextMixin):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        query = self.request.GET.get("query")
        context["query"] = query
        context["search_form"] = SearchForm(self.request.GET) if query else SearchForm()
        resolved = resolve(self.request.path_info)
        context["route_name"] = resolved.url_name
        return context

    @staticmethod
    def calculate_similarity(query, queryset):
        if query:
            A = 1.0
            B = 0.4
            title_similarity = A / (A + B) * TrigramSimilarity('title', query)
            content_similarity = B / (A + B) * TrigramWordSimilarity(query, 'content')
            queryset = queryset.annotate(
                similarity=title_similarity+content_similarity).filter(similarity__gte=0.2).order_by('-similarity')

        return queryset
