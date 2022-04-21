from django.urls import path

from . import views


urlpatterns = [
    path('', views.LotListView.as_view(), name='lots'),
    path('<int:pk>/', views.LotDetailView.as_view(), name='lot'),
]