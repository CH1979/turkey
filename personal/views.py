from django.http import JsonResponse
from django.urls import reverse
from django.views.generic import CreateView, DetailView

from .models import Profile


class ProfileDetailView(DetailView):
    model = Profile
    fields = '__all__'


class ProfileCreateView(CreateView):
    model = Profile
    fields = ('phone')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('index')
