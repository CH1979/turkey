from django.db.models import Q
from django.http import JsonResponse
from django.urls import reverse
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView
)
from django.views.generic.base import TemplateView

from . import models


class LotDetailView(DetailView):
    """Представление для одного объявления"""
    model = models.Lot

    def get_context_data(self, **kwargs):
        context = super(DetailView, self).get_context_data(**kwargs)
        context['category_list'] = models.Category.get_root_nodes()
        return context


class LotListView(ListView):
    """Представление для списка объявлений"""
    model = models.Lot

    def get_context_data(self, **kwargs):
        context = super(LotListView, self).get_context_data(**kwargs)
        category_id = self.kwargs.get('pk', None)

        # Создание списка категорий для бокового меню
        if category_id is not None:
            current_category = models.Category.objects.get(id=category_id)
            context['current_category'] = current_category
            context['category_list'] = current_category.get_siblings()
            context['category_children'] = current_category.get_children()
        else:
            context['category_list'] = models.Category.get_root_nodes()

        return context
    
    def get_queryset(self):
        queryset = super().get_queryset()
        category_id = self.kwargs.get('pk', None)

        # Фильтрация кверисета по категории, если она задана
        if category_id is not None:
            current_category = models.Category.objects.get(id=category_id)
            category_descendants = current_category.get_descendants()
            queryset = queryset.filter(
                Q(category__in=category_descendants) | Q(category=current_category)
            )

        return queryset


class LotCreateView(CreateView):
    """Представление для создания объявления"""
    template_name = 'market/lot_create.html'
    model = models.Lot
    fields = [
        'title',
        'category',
        'price',
        'currency',
        'description',
        'extra_fields',
        'video_url',
    ]

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_success_url(self, **kwargs):
        return reverse('gallery', kwargs={'pk': self.object.pk})


class GalleryListView(ListView):
    """Представление фото объявления"""
    model = models.Gallery
    fields = ('image', )
    template_name = 'market/gallery.html'

    def get_queryset(self):
        pk = self.kwargs['pk']
        queryset = super().get_queryset().filter(lot_id=pk)
        return queryset


class GalleryCreateView(CreateView):
    """Представление для добавления фото объявления"""
    model = models.Gallery
    fields = ('image', )

    def post(self, request, *args, **kwargs):
        pk = self.kwargs['pk']
        lot = models.Lot.objects.get(pk=pk)

        gallery = []

        for image in request.FILES.values():
            gallery.append(models.Gallery(lot=lot, image=image))

        models.Gallery.objects.bulk_create(gallery)

        return JsonResponse({'status': 'OK'})


class GalleryDeleteView(DeleteView):
    """Представление для удаления фото объявления"""
    model = models.Gallery

    def get_success_url(self):
        lot = self.kwargs['lot']
        return reverse('gallery', kwargs={'pk': lot})
