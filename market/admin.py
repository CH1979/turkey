from django.contrib import admin
from treebeard.admin import TreeAdmin
from treebeard.forms import movenodeform_factory

from . import models


class CategoryAdmin(TreeAdmin):
    form = movenodeform_factory(models.Category)


@admin.register(models.ExtraField)
class ExtraFieldAdmin(admin.ModelAdmin):
    add_form_template = 'change_extra_field_form.html'
    change_form_template = 'change_extra_field_form.html'


admin.site.register(models.Category, CategoryAdmin)
admin.site.register(models.Currency)
admin.site.register(models.Lot)
