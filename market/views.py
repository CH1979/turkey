from django.db.models import Q
from django.views.generic import DetailView, ListView
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
        if category_id is not None:
            current_category = models.Category.objects.get(id=category_id)
            category_descendants = current_category.get_descendants()
            queryset = queryset.filter(
                Q(category__in=category_descendants) | Q(category=current_category)
            )
        return queryset


class CategoryView(TemplateView):
    template_name = "categories.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = models.Category.dump_bulk()
        return context
