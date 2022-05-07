from django.urls import path

from . import views


urlpatterns = [
    # Объявления ##############################
    # Список объявлений
    path(
        '',
        views.LotListView.as_view(),
        name='market'
    ),
    path(
        'category/select/',
        views.category_select,
        name='category_select'
    ),
        path(
        'location/select/',
        views.location_select,
        name='location_select'
    ),
    # Создание объявления
    path(
        'lot/create/',
        views.LotCreateView.as_view(),
        name='lot_create',
    ),
    # Просмотр объявления
    path(
        '<int:pk>/',
        views.LotDetailView.as_view(),
        name='lot_detail'
    ),
    # Список объявлений по категории
    path(
        'category/<int:pk>/',
        views.LotListView.as_view(),
        name='category_detail'
    ),
    # Удаление объявления
    path(
        '<int:pk>/delete/',
        views.LotDeleteView.as_view(),
        name='lot_delete'
    ),
    # Добавление в избранное
    path(
        '<int:pk>/favorite/',
        views.lot_favorite,
        name='lot_favorite'
    ),
    # Удаление из избранного
    path(
        '<int:pk>/unfavorite/',
        views.lot_unfavorite,
        name='lot_unfavorite'
    ),


    # Фото объявления #########################
    # Список фото
    path(
        '<int:pk>/gallery/',
        views.GalleryListView.as_view(),
        name='gallery'
    ),
    # Добавление фото
    path(
        '<int:pk>/gallery/create/',
        views.GalleryCreateView.as_view(),
        name='gallery_create'
    ),
    # Удаление фото
    path(
        '<int:lot>/gallery/<int:pk>/delete/',
        views.GalleryDeleteView.as_view(),
        name='gallery_delete'
    )
]