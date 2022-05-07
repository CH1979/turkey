import os
from uuid import uuid4

from django.db import models
from django.contrib.auth.models import User
from stdimage import StdImageField
from treebeard.mp_tree import MP_Node
from treewidget.fields import TreeForeignKey


def image_rename(instance, filename):
    """Переименовывает загружаемые изображения.
    В изображениях, полученных из JS-скрипта обрезается часть
    имени файла, добавленная скриптом (:upload...)"""
    if ':' in filename:
        filename = filename.split(':')[0]
    _, ext = os.path.splitext(filename)
    name = uuid4().hex
    filename = "{}{}".format(name, ext)
    return os.path.join('images', 'market', filename)


class ExtraField(models.Model):
    """Наборы дополнительных полей"""
    description = models.JSONField(
        verbose_name='описание набора',
        null=False,
        blank=False,
    )

    class Meta:
        verbose_name = 'набор дополнительных полей'
        verbose_name_plural = 'наборы дополнительных полей'

    def __str__(self):
        desc = ', '.join([str(x['name']) for x in self.description])
        return desc


class Category(MP_Node):
    """Категория объявления"""
    name = models.CharField(
        verbose_name='название',
        max_length=50,
        unique=True
    )
    extra_fields = models.ForeignKey(
        to=ExtraField,
        verbose_name='дополнительные поля',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )

    node_order_by = ['name']

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'категории'

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        """При сохранении модели добавляем такой же набор дополнительных полей
        всем дочерним категориям
        """
        self.get_descendants().update(extra_fields=self.extra_fields)
        return super().save(*args, **kwargs)


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
    rate = models.DecimalField(
        verbose_name='курс обмена',
        max_digits=10,
        decimal_places=4,
    )

    class Meta:
        verbose_name = 'валюта'
        verbose_name_plural = 'валюты'

    def __str__(self):
        return self.name


class Lot(models.Model):
    """Объявление"""
    title = models.CharField(
        verbose_name='заголовок',
        max_length=150,
        blank=False,
        null=False,
    )
    category = TreeForeignKey(
        to=Category,
        verbose_name='категория',
        blank=False,
        null=False,
        on_delete=models.CASCADE,
        settings={ 'filtered': True },
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
        auto_now=True,
    )
    price = models.DecimalField(
        verbose_name='цена',
        blank=False,
        null=False,
        max_digits=12,
        decimal_places=2,
    )
    currency = models.ForeignKey(
        to=Currency,
        verbose_name='валюта',
        blank=False,
        null=False,
        on_delete=models.CASCADE
    )
    description = models.TextField(
        verbose_name='описание'
    )
    extra_fields = models.JSONField(
        verbose_name='дополнительные поля',
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
        ordering = ['-created_at']

    def __str__(self):
        return '{} - {}'.format(self.id, self.title)


class Gallery(models.Model):
    """
    Галерея изображений
    """
    lot = models.ForeignKey(
        to=Lot,
        verbose_name='объявление',
        null=False,
        blank=False,
        on_delete=models.CASCADE
    )
    image = StdImageField(
        verbose_name='изображение',
        upload_to=image_rename,
        null=True,
        blank=True,
        variations={
            'medium': (336, 336),
            'square_thumbnail': (336, 336, True),
            'square_medium': (696, 696, True),
        },
        delete_orphans=True
    )

    class Meta:
        verbose_name = 'галерея'
        verbose_name_plural = 'галереи'

    def __str__(self):
        return '{} - {}'.format(self.lot, self.id)
