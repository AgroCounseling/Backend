from django.db import models
from django.contrib.auth import settings
from django.utils.translation import gettext_lazy as _
from categories.models import *


class Forum(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name=_('Пользователь'))
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name=_('Категории'))
    subcategory = models.ForeignKey(SubCategory, on_delete=models.CASCADE, verbose_name=_('Подкатегории'), blank=True,
                                    null=True)
    types = models.ForeignKey(Types, on_delete=models.CASCADE, verbose_name=_('Виды'), blank=True, null=True)
    subtypes = models.ForeignKey(SubTypes, on_delete=models.CASCADE, verbose_name=_('Подвиды'), blank=True, null=True)
    title = models.TextField(max_length=5000, verbose_name=_('Вопрос'))
    pub_date = models.DateField(auto_now_add=True, verbose_name=_('Дата публикации'))

    class Meta:
        verbose_name = _('Вопрос')
        verbose_name_plural = _('Вопросы')
        ordering = ['-pub_date']

    def __str__(self):
        return self.title


class Comment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name=_('Пользователь'))
    forum = models.ForeignKey(Forum, on_delete=models.CASCADE, related_name='comments', verbose_name=_('Форум'))
    description = models.TextField(max_length=5000, verbose_name=_('Комментарии'))
    pub_date = models.DateField(auto_now_add=True, verbose_name=_('Дата публикации'))

    class Meta:
        verbose_name = _('Комментарии')
        verbose_name_plural = _('Комментарии')

    def __str__(self):
        return '{}'.format(self.user)
