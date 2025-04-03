from django.db import models


class ServiceCategory(models.Model):
    name = models.CharField('Название категории', max_length=200, unique=True)
    description = models.TextField('Описание')
    slug = models.SlugField('Slug', unique=True, blank=True)

    class Meta:
        verbose_name = 'Категория услуги'
        verbose_name_plural = 'Категории услуг'
        ordering = ['name']

    def __str__(self):
        return self.name


class Service(models.Model):
    name = models.CharField('Название услуги', max_length=200, unique=True)
    description = models.TextField('Описание')
    category = models.ForeignKey(
        ServiceCategory,
        on_delete=models.CASCADE,
        related_name='services',
        verbose_name='Категория услуги'
    )
    slug = models.SlugField('Slug', unique=True, blank=True)

    class Meta:
        verbose_name = 'Услуга'
        verbose_name_plural = 'Услуги'
        ordering = ['name']

    def __str__(self):
        return self.name
