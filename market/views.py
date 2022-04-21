from django.views.generic import DetailView, ListView

from . import models


class LotDetailView(DetailView):
    """Представление для одного объявления"""
    model = models.Lot


class LotListView(ListView):
    """Представление для списка объявлений"""
    model = models.Lot

    def get_context_data(self, **kwargs):
        context = super(LotListView, self).get_context_data(**kwargs)
        context['category_list'] = models.Category.get_root_nodes()
        return context
