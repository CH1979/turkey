import os
from uuid import uuid4

from ckeditor_uploader.fields import RichTextUploadingField
from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from stdimage import StdImageField
from taggit.managers import TaggableManager


def image_rename(instance, filename):
    """Переименовывает загружаемые изображения.
    В изображениях, полученных из JS-скрипта обрезается часть
    имени файла, добавленная скриптом (:upload...)"""
    if ':' in filename:
        filename = filename.split(':')[0]
    _, ext = os.path.splitext(filename)
    name = uuid4().hex
    filename = "{}{}".format(name, ext)
    return os.path.join('images', 'articles', filename)


class Rubric(models.Model):
    """Рубрика статьи"""
    name = models.CharField(
        verbose_name='название рубрики',
        max_length=20,
        blank=False,
        null=False,
    )
    on_main = models.BooleanField(
        verbose_name='отображать на главной',
        blank=False,
        null=False,
        default=False,
    )

    class Meta:
        verbose_name = 'рубрика'
        verbose_name_plural = 'рубрики'
        ordering = ['-on_main', 'name']

    def __str__(self):
        return self.name + (' - на главной' if self.on_main else '')


class Article(models.Model):
    """Статья"""
    title = models.CharField(
        verbose_name='заголовок',
        max_length=100,
        blank=False,
        null=False,
    )
    cover = StdImageField(
        verbose_name='титульное изображение',
        upload_to=image_rename,
        null=True,
        blank=True,
        variations={
            'main': (900, 500, True),
            'half_size': (450, 250, True),
        },
        delete_orphans=True
    )
    rubric = models.ForeignKey(
        to=Rubric,
        verbose_name='рубрика',
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
    )
    author = models.ForeignKey(
        to=User,
        verbose_name='автор',
        blank=True,
        null=True,
        on_delete=models.SET_NULL
    )
    created_at = models.DateTimeField(
        verbose_name='создано',
        auto_now=True,
    )
    content = RichTextUploadingField()
    tags = TaggableManager()
    is_draft = models.BooleanField(
        verbose_name='черновик',
        null=False,
        blank=False,
        default=True
    )

    class Meta:
        verbose_name = 'статья'
        verbose_name_plural = 'статьи'
        ordering = ['-created_at']

    def __str__(self):
        return self.title + (' - черновик' if self.is_draft else '')

    def get_absolute_url(self):
        return reverse('article_detail', kwargs={'pk': self.pk})
