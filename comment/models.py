from django.db import models
from elon.models import Elon


class Comment(models.Model):
    elon = models.ForeignKey(Elon, on_delete=models.CASCADE, verbose_name='E`lon')
    author = models.CharField(max_length=30, verbose_name='author')
    body = models.TextField(verbose_name='Comment body')
    is_active = models.BooleanField(default=True, verbose_name='Ekranga chiqsinmi?')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='yozilgan sana')

    class Meta:
        verbose_name = 'Kommentariya'
        verbose_name_plural = 'Kommentariyalar'
        ordering = ['created_at']

    def __str__(self):
        return f"{self.author}-{self.body[:15]}"
