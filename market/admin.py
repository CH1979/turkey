from django.contrib import admin
from treebeard.admin import TreeAdmin
from treebeard.forms import movenodeform_factory

from . import models


class CategoryAdmin(TreeAdmin):
    form = movenodeform_factory(models.Category)


admin.site.register(models.Category, CategoryAdmin)
admin.site.register(models.Currency)
admin.site.register(models.Lot)
