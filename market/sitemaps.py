from django.contrib.sitemaps import Sitemap

from .models import Lot


class LotViewSitemap(Sitemap):
    changefreq = "never"
    priority = 0.5

    def items(self):
        return Lot.objects.all()

    def lastmod(self, obj):
        return obj.created_at
