from django.forms import ModelForm

from .models import Lot

class CategoryForm(ModelForm):
    class Meta:
        model = Lot
        fields = ['category', ]
