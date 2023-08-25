from django.db import models
from .managers import SuperCategoryManager, ChildCategoryManager


class Category(models.Model):
    name = models.CharField(max_length=50, verbose_name='Category nomi', unique=True)
    order = models.SmallIntegerField(default=0, verbose_name='navbati')
    parent_category = models.ForeignKey('SuperCategory', on_delete=models.PROTECT, null=True, blank=True,
                                       verbose_name='Super category')


class SuperCategory(Category):
    objects = SuperCategoryManager()

    def __str__(self):
        return self.name

    class Meta:
        proxy = True
        ordering = ['order', 'name']
        verbose_name = 'Super Category'
        verbose_name_plural = 'Super Categoriyalar'


class ChildCategory(Category):
    objects = ChildCategoryManager()

    def __str__(self):
        return f"{self.parent_category.name}-{self.name}"

    class Meta:
        proxy = True
        ordering = ['parent_category__order', 'order', 'name']
        verbose_name = 'Bola Category'
        verbose_name_plural = 'Bola Categoriyalar'
