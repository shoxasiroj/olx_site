from django.db import models


class SuperCategoryManager(models.Manager):

    # Otasi bormi diganda ha degan tekshiruv
    def get_queryset(self):
        return super().get_queryset().filter(parent_category__isnull=True)


class ChildCategoryManager(models.Manager):

    # Otasi bormi diagnda yo`q digan tekshiruv
    def get_queryset(self):
        return super().get_queryset().filter(parent_category__isnull=False)
