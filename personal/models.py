import os
from uuid import uuid4

from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from phonenumber_field.modelfields import PhoneNumberField
from treebeard.mp_tree import MP_Node
from treewidget.fields import TreeForeignKey

from market.models import Lot


def image_rename(instance, filename):
    """Переименовывает загружаемые изображения.
    В изображениях, полученных из JS-скрипта обрезается часть
    имени файла, добавленная скриптом (:upload...)"""
    if ':' in filename:
        filename = filename.split(':')[0]
    _, ext = os.path.splitext(filename)
    name = uuid4().hex
    filename = "{}{}".format(name, ext)
    return os.path.join('images', 'profile', filename)


class Location(MP_Node):
    """Регион"""
    name = models.CharField(
        max_length=30,
        verbose_name='наименование',
        null=False,
        blank=False,
    )
    status = models.CharField(
        max_length=20,
        verbose_name='статус',
        null=False,
        blank=False,
    )

    class Meta:
        verbose_name = 'регион'
        verbose_name_plural = 'регионы'
        ordering = ['name']

    def __str__(self):
        return '{} {}'.format(self.status, self.name)


class Profile(models.Model):
    """Дополнительный профиль для маркета"""
    user = models.OneToOneField(
        to=User,
        verbose_name='пользователь',
        null=False,
        blank=False,
        on_delete=models.CASCADE
    )
    phone = PhoneNumberField(
        verbose_name='номер телефона',
        blank=True,
        null=True,
    )
    location = TreeForeignKey(
        to=Location,
        verbose_name='регион',
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
    )
    lot = models.ManyToManyField(
        to=Lot,
        verbose_name='избранное объявление',
        blank=True,
    )

    class Meta:
        verbose_name = 'профиль пользователя'
        verbose_name_plural = 'профили пользователя'
        ordering = ['user']

    def __str__(self):
        return self.user.username


@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    profile = Profile.objects.get_or_create(user=instance)
    instance.profile.save()
