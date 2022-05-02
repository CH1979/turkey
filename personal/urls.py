from django.urls import path

from . import views


urlpatterns = [
    path(
        'create/',
        views.ProfileCreateView.as_view(),
        name='profile_create',
    ),
    path(
        '<int:pk>/my_lots/',
        views.ProfileMyLotsView.as_view(),
        name='my_lots',
    ),
    path(
        '<int:pk>/favorite_lots/',
        views.ProfileFavoriteLotsView.as_view(),
        name='favorite_lots',
    ),
    path(
        '<int:pk>/my_topics/',
        views.ProfileMyTopicsView.as_view(),
        name='my_topics',
    ),
    path(
        '<int:pk>/favorite_topics/',
        views.ProfileFavoriteTopicsView.as_view(),
        name='favorite_topics',
    )

]