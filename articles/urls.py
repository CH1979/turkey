from django.urls import path

from . import views


urlpatterns = [
    path(
        '',
        views.ArticleMainView.as_view(),
        name='articles',
    ),
    path(
        '<int:pk>/',
        views.ArticleDetailView.as_view(),
        name='article_detail',
    ),
    path(
        'rubric/<int:pk>/',
        views.ArticlesByRubricView.as_view(),
        name='articles_by_rubric',
    ),
    path(
        'tag/<int:pk>/',
        views.ArticlesByTagView.as_view(),
        name='articles_by_tag',
    )
]