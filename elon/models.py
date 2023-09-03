from main.models import AdvUser
from django.db import models
from category.models import ChildCategory
from .utilities import get_timed_path


class Elon(models.Model):
    COUNTRY_CHOICES = (
        ('+1', 'USA'),
        ('+44', 'UK'),
        ('+33', 'France'),
        ('+99', 'UZ'),
        ('+7', 'RU'),
        ('+7', 'QZ'),
    )
    category = models.ForeignKey(ChildCategory, on_delete=models.CASCADE, null=True, blank=True,
                                 verbose_name='Elon category')
    title = models.CharField(max_length=155, verbose_name='Elonning nomi')
    body = models.TextField(verbose_name='Elonning contenti')
    price = models.FloatField(blank=True, null=True, verbose_name='Narxi')
    country_code = models.CharField(max_length=5, choices=COUNTRY_CHOICES)
    image = models.ImageField(upload_to=get_timed_path, blank=True, verbose_name='rasm')
    author = models.ForeignKey(AdvUser, on_delete=models.CASCADE, null=True, blank=True,
                               verbose_name='Aftor')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def delete(self, *args, **kwargs):
        for image in self.additionalimage_set.all():
            image.delete()
        super().delete(*args, **kwargs)

    class Meta:
        verbose_name = 'E`lon'
        verbose_name_plural = 'E`lonlar'
        ordering = ['-created_at']


class AdditionalImage(models.Model):
    elon = models.ForeignKey(Elon, on_delete=models.CASCADE, verbose_name='elon')
    image = models.ImageField(upload_to=get_timed_path, blank=True, verbose_name='qo`shimcha rasm')

    class Meta:
        verbose_name = 'Qo`shimcha rasm'
        verbose_name_plural = 'Qo`shimcha rasmlar'
