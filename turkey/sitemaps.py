from django.contrib.sitemaps import Sitemap
from django.urls import reverse


class ForumSitemap(Sitemap):
    changefreq = "daily"
    priority = 0.5

    def items(self):
        return ['forum:index',]

    def location(self, item):
        return reverse(item)
