"""turkey URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.sitemaps import views as sitemap_views
from django.views.generic.base import RedirectView
from django.urls import path, include
from machina import urls as machina_urls

from articles.sitemaps import ArticleViewSitemap
from market.sitemaps import LotViewSitemap
from .sitemaps import ForumSitemap
from .views import AgreementView, PrivacyView


sitemaps = {
    'market': LotViewSitemap,
    'articles': ArticleViewSitemap,
    'forum': ForumSitemap,
}

urlpatterns = [
    path(
        'admin/',
        admin.site.urls
    ),
    path(
        'accounts/',
        include('allauth.urls')
    ),
    path(
        'accounts/profile/',
        include('personal.urls')
    ),
    path(
        'articles/',
        include('articles.urls')
    ),
    path(
        'forum/',
        include(machina_urls)
    ),
    path(
        'market/',
        include('market.urls')
    ),
    path(
        'treewidget/',
        include('treewidget.urls')
    ),
    path(
        'ckeditor/',
        include('ckeditor_uploader.urls')
    ),
    path(
        'captcha/',
        include('captcha.urls')
    ),
    path(
        'search/',
        include('haystack.urls')
    ),
    path(
        'sitemap.xml',
        sitemap_views.index,
        {'sitemaps': sitemaps},
    ),
    path(
        'sitemap-<section>.xml',
        sitemap_views.sitemap,
        {'sitemaps': sitemaps},
        name='django.contrib.sitemaps.views.sitemap',
    ),
    path(
        'privacy',
        PrivacyView.as_view(),
        name='privacy'
    ),
    path(
        'agreement',
        AgreementView.as_view(),
        name='agreement'
    ),
    path(
        '',
        RedirectView.as_view(pattern_name='market', permanent=False),
        name='index'
    ),
]

if True: # settings.DEBUG:
    urlpatterns = urlpatterns + static(
        settings.STATIC_URL,
        document_root=settings.STATIC_ROOT
    )
    urlpatterns = urlpatterns + static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )


handler404 = "turkey.views.page_not_found_view"

handler500 = "turkey.views.error_view"

handler403 = "turkey.views.permission_denied_view"

handler400 = "turkey.views.bad_request_view"
