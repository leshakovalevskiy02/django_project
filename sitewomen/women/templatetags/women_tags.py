from django import template
from women.models import Category, TagPost, Women
from django.db.models import Count
# from women.utils import menu


register = template.Library()


# @register.simple_tag
# def get_menu():
#     return menu


@register.inclusion_tag("women/list_categories.html")
def show_categories(cat_selected=0):
    cats = Category.objects.filter(where_posts__is_published=Women.Status.PUBLISHED).annotate(
                                            total=Count("where_posts")).filter(total__gt=0)

    return {"cats": cats, "cat_selected": cat_selected}


@register.inclusion_tag("women/list_tags.html")
def show_tags():
    tags = TagPost.objects.filter(tags__is_published=Women.Status.PUBLISHED).annotate(
                                        total=Count("tags")).filter(total__gt=0)

    return {"tags": tags}