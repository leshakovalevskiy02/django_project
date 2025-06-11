from django.contrib.sitemaps import Sitemap
from .models import Women, Category


info_dict = {
    "queryset": Women.published.all(),
    "date_field": "time_update"
}


class CategorySitemap(Sitemap):
    changefreq = "monthly"
    priority = 0.7

    def items(self):
        return Category.objects.all()

    def lastmod(self, obj):
        return max(obj.posts.all(), key=lambda post: post.time_update).time_update