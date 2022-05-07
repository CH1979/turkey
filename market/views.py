from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.http import Http404, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView
)

from . import models
from .forms import CategoryForm, LocationForm, LotForm
from personal.models import Location, Profile


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
    paginate_by = 12

    def get_context_data(self, **kwargs):
        context = super(LotListView, self).get_context_data(**kwargs)
        category_id = self.kwargs.get('pk', None)
        location_id = self.request.session.get('location_id', None)

        # Создание списка категорий для бокового меню
        if category_id is not None:
            current_category = models.Category.objects.get(id=category_id)
            context['current_category'] = current_category
            context['category_list'] = current_category.get_siblings()
            context['category_children'] = current_category.get_children()
        else:
            context['category_list'] = models.Category.get_root_nodes()

        if location_id is not None:
            current_location = Location.objects.get(id=location_id)
            location_descendants = current_location.get_descendants()
            context['current_location'] = current_location
            context['location_descendants'] = location_descendants

        return context
    
    def get_queryset(self):
        queryset = super().get_queryset()
        category_id = self.kwargs.get('pk', None)
        location_id = self.request.session.get('location_id', None)

        # Фильтрация кверисета по категории, если она задана
        if category_id is not None:
            current_category = models.Category.objects.get(id=category_id)
            category_descendants = current_category.get_descendants()
            queryset = queryset.filter(
                Q(category__in=category_descendants) | Q(category=current_category)
            )

        if location_id is not None:
            current_location = Location.objects.get(id=location_id)
            location_descendants = current_location.get_descendants()
            authors = Profile.objects.filter(
                Q(location__in=location_descendants) \
                    | Q(location=current_location)
            )
            queryset = queryset.filter(author__profile__in=authors)

        return queryset


@login_required
def category_select(request):
    form = CategoryForm(request.POST or None)

    if request.method == 'POST':
        if form.is_valid():
            if form.cleaned_data['category'] is not None:
                request.session['category_id'] = form.cleaned_data['category'].id
                return HttpResponseRedirect(reverse('lot_create'))

    return render(request, 'market/category_select.html', {'form': form})


def location_select(request):
    form = LocationForm(request.POST or None)

    if request.method == 'POST':
        if form.is_valid():
            if form.cleaned_data['location'] is not None:
                request.session['location_id'] = form.cleaned_data['location'].id
                return HttpResponseRedirect(reverse('market'))

    return render(request, 'market/location_select.html', {'form': form})


class LotCreateView(LoginRequiredMixin, CreateView):
    """Представление для создания объявления"""
    template_name = 'market/lot_create.html'
    model = models.Lot
    form_class = LotForm

    def form_valid(self, form):
        category_id = self.request.session['category_id']

        form.instance.category = models.Category.objects.get(id=category_id)
        form.instance.author = self.request.user
        return super().form_valid(form)


    def get_success_url(self, **kwargs):
        return reverse('gallery', kwargs={'pk': self.object.pk})


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        category_id = self.request.session['category_id']
        try:
            extra_fields = models.ExtraField.objects.get(category=category_id)
            context['extra_fields'] = extra_fields
        except models.ExtraField.DoesNotExist:
            context['extra_fields'] = ''

        return context


class LotDeleteView(LoginRequiredMixin, DeleteView):
    """Представление для удаления объявления"""
    model = models.Lot

    def get_success_url(self):
        return reverse('profile', kwargs={'pk': self.request.user.profile.id})


@login_required
def lot_favorite(request, pk):
    if request.method == 'GET':
        raise Http404

    if request.method == 'POST':
        user = request.user
        profile = Profile.objects.get(user=user)
        lot = models.Lot.objects.get(id=pk)
        profile.lot.add(lot)

        return JsonResponse({'status': 'OK'})


@login_required
def lot_unfavorite(request, pk):
    if request.method == 'GET':
        raise Http404

    if request.method == 'POST':
        user = request.user
        profile = Profile.objects.get(user=user)
        lot = models.Lot.objects.get(id=pk)
        profile.lot.remove(lot)

        return JsonResponse({'status': 'OK'})


class GalleryListView(LoginRequiredMixin, ListView):
    """Представление фото объявления"""
    model = models.Gallery
    fields = ('image', )
    template_name = 'market/gallery.html'

    def get_queryset(self):
        pk = self.kwargs['pk']
        queryset = super().get_queryset().filter(lot_id=pk)
        return queryset


class GalleryCreateView(LoginRequiredMixin, CreateView):
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


class GalleryDeleteView(LoginRequiredMixin, DeleteView):
    """Представление для удаления фото объявления"""
    model = models.Gallery

    def get_success_url(self):
        lot = self.kwargs['lot']
        return reverse('gallery', kwargs={'pk': lot})
