from django.urls import path

from . import views


urlpatterns = [
    path(
        '',
        views.LotListView.as_view(),
        name='market'
    ),
    path(
        '<int:pk>/',
        views.LotDetailView.as_view(),
        name='lot-detail'
    ),
    path(
        'category/<int:pk>/',
        views.LotListView.as_view(),
        name='category-detail'
    ),
    path(
        'categories/',
        views.CategoryView.as_view(),
        name='market-categories'
    ),
]