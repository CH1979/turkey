from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views.generic import DetailView

from .forms import UserForm, ProfileForm, ForumProfileForm
from .models import Profile


class ProfileDetailView(LoginRequiredMixin, DetailView):
    model = Profile
    fields = '__all__'


class ProfileMyLotsView(LoginRequiredMixin, DetailView):
    model = Profile
    fields = '__all__'
    template_name = 'personal/profile_my_lots.html'


class ProfileFavoriteLotsView(LoginRequiredMixin, DetailView):
    model = Profile
    fields = '__all__'
    template_name = 'personal/profile_favorite_lots.html'


class ProfileMyTopicsView(LoginRequiredMixin, DetailView):
    model = Profile
    fields = '__all__'
    template_name = 'personal/profile_my_topics.html'


class ProfileFavoriteTopicsView(LoginRequiredMixin, DetailView):
    model = Profile
    fields = '__all__'
    template_name = 'personal/profile_favorite_topics.html'


@login_required
@transaction.atomic
def update_profile(request):
    if request.method == 'POST':
        user_form = UserForm(
            request.POST,
            instance=request.user
        )
        profile_form = ProfileForm(
            request.POST,
            instance=request.user.profile
        )
        forum_profile_form = ForumProfileForm(
            request.POST,
            instance=request.user.forum_profile
        )
        if user_form.is_valid() and profile_form.is_valid() \
            and forum_profile_form.is_valid():

            user_form.save()
            profile_form.save()
            forum_profile_form.save()

            return HttpResponseRedirect(
                reverse('profile_detail', kwargs={'pk': request.user.profile.id})
                )
    else:
        user_form = UserForm(
            instance=request.user
        )
        profile_form = ProfileForm(
            instance=request.user.profile
        )
        forum_profile_form = ForumProfileForm(
            instance=request.user.forum_profile
        )
    return render(
        request,
        'personal/profile_form.html',
        {
            'user_form': user_form,
            'profile_form': profile_form,
            'forum_profile_form': forum_profile_form
        })