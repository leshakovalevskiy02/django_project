from django.views.generic.base import ContextMixin


class DataMixin(ContextMixin):
    extra_context = {}
    title = None
    paginate_by = 4

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