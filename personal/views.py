from django.http import JsonResponse
from django.urls import reverse
from django.views.generic import CreateView, DetailView

from .models import Profile


class ProfileMyLotsView(DetailView):
    model = Profile
    fields = '__all__'
    template_name = 'personal/profile_my_lots.html'


class ProfileFavoriteLotsView(DetailView):
    model = Profile
    fields = '__all__'
    template_name = 'personal/profile_favorite_lots.html'


class ProfileMyTopicsView(DetailView):
    model = Profile
    fields = '__all__'
    template_name = 'personal/profile_my_topics.html'


class ProfileFavoriteTopicsView(DetailView):
    model = Profile
    fields = '__all__'
    template_name = 'personal/profile_favorite_topics.html'


class ProfileCreateView(CreateView):
    model = Profile
    fields = ('phone')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('index')
