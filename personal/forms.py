from django import forms
from django.contrib.auth.models import User
from machina.apps.forum_member.models import ForumProfile

from .models import Profile


CSS_CLASSES = "form-control form-control-lg text-4"


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')

    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = CSS_CLASSES


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('phone', 'location')

    def __init__(self, *args, **kwargs):
        super(ProfileForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = CSS_CLASSES


class ForumProfileForm(forms.ModelForm):
    class Meta:
        model = ForumProfile
        fields = ('avatar', )

    def __init__(self, *args, **kwargs):
        super(ForumProfileForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = CSS_CLASSES
