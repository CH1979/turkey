from captcha.fields import CaptchaField
from django.forms import ModelForm

from .models import Lot


CSS_CLASSES = "form-control form-control-lg text-4"


class CategoryForm(ModelForm):
    class Meta:
        model = Lot
        fields = ['category', ]


class LotForm(ModelForm):
    captcha = CaptchaField()

    class Meta:
        model = Lot
        fields = [
            'title',
            'price',
            'currency',
            'description',
            'extra_fields',
            'video_url',
        ]

    def __init__(self, *args, **kwargs):
        super(LotForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            if visible.name == 'captcha':
                visible.field.widget.attrs['class'] = CSS_CLASSES
