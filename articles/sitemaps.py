from django.contrib.sitemaps import Sitemap

from .models import Article


class ArticleViewSitemap(Sitemap):
    changefreq = "never"
    priority = 0.5

    def items(self):
        return Article.objects.filter(is_draft=False)

    def lastmod(self, obj):
        return obj.created_at
