import os
from uuid import uuid4

from django.db import models
from django.contrib.auth.models import User
from treebeard.mp_tree import MP_Node


def image_rename(instance, filename):
    """Переименовывает загружаемые изображения"""
    _, ext = os.path.splitext(filename)
    name = uuid4().hex
    filename = "{}{}".format(name, ext)
    return os.path.join('images', filename)


class Category(MP_Node):
    """Категория объявления"""
    name = models.CharField(
        verbose_name='название',
        max_length=50,
        unique=True
    )

    node_order_by = ['name']

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'категории'

    def __str__(self):
        return self.name


class Currency(models.Model):
    """Валюта"""
    name = models.CharField(
        max_length=30,
        verbose_name='название',
        blank=False,
        null=False
    )
    symbol = models.CharField(
        max_length=1,
        verbose_name='символ',
    )
    rate = models.FloatField(
        verbose_name='курс обмена',
    )

    class Meta:
        verbose_name = 'валюта'
        verbose_name_plural = 'валюты'

    def __str__(self):
        return self.name


# class Location(models.Model):
#     pass

    # class Meta:
    #     verbose_name = ''
    #     verbose_name_plural = ''

    # def __str__(self):
    #     return '% - %'.format(self.lot, self.id)


class Lot(models.Model):
    """Объявление"""
    title = models.CharField(
        verbose_name='заголовок',
        max_length=50,
        blank=False,
        null=False,
    )
    category = models.ForeignKey(
        to=Category,
        verbose_name='категория',
        blank=False,
        null=False,
        on_delete=models.CASCADE
    )
    author = models.ForeignKey(
        to=User,
        verbose_name='автор',
        blank=False,
        null=False,
        on_delete=models.CASCADE
    )
    created_at = models.DateTimeField(
        verbose_name='создано',
        auto_now_add=True,
    )
    price = models.IntegerField(
        verbose_name='цена',
        blank=False,
        null=False,
    )
    currency = models.ForeignKey(
        to=Currency,
        verbose_name='валюта',
        blank=False,
        null=False,
        on_delete=models.CASCADE
    )
    # location = models.ForeignKey(
    #     verbose_name='местоположение'
    # )
    description = models.TextField(
        verbose_name='описание'
    )
    thumbnail = models.ImageField(
        verbose_name='превью',
        upload_to=image_rename,
        null=True,
        blank=True,
    )
    video_url = models.URLField(
        verbose_name='видео',
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name = 'объявление'
        verbose_name_plural = 'объявления'

    def __str__(self):
        return '{} - {}'.format(self.id, self.title)


class Gallery(models.Model):
    """
    Изображение объявления
    """
    lot = models.ForeignKey(
        to=Lot,
        verbose_name='объявление',
        null=False,
        blank=False,
        on_delete=models.CASCADE
    )
    image = models.ImageField(
        verbose_name='изображение',
        null=False,
        blank=False
    )
    thumbnail = models.ImageField(
        verbose_name='превью',
        null=False,
        blank=False
    )

    class Meta:
        verbose_name = 'изображение'
        verbose_name_plural = 'изображения'

    def __str__(self):
        return '{} - {}'.format(self.lot, self.id)
