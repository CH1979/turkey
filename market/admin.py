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


class ImagesInline(admin.TabularInline):
    model = models.Gallery


@admin.register(models.Lot)
class LotAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'category',
        'author',
        'created_at',
        'price',
        'currency',
        'description',
        'extra_fields',
        'video_url',
    )
    inlines = [ImagesInline]


admin.site.register(models.Category, CategoryAdmin)
admin.site.register(models.Currency)
