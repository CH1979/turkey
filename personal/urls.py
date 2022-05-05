from django.urls import path

from . import views


urlpatterns = [
    path(
        '<int:pk>/',
        views.ProfileDetailView.as_view(),
        name='profile_detail',
    ),
    path(
        'profile_update/',
        views.update_profile,
        name='profile_update',
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