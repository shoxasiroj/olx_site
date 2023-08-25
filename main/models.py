from django.db import models
from django.contrib.auth.models import AbstractUser


class AdvUser(AbstractUser):
    is_activated = models.BooleanField(default=True, verbose_name='Aktivatsiya qilinganmi')
    send_message = models.BooleanField(default=True, verbose_name='Yangi koment kelganda hat kelsin')

    def delete(self, *args, **kwargs):
        for elon in self.elon_set.all():
            elon.delete()
        super().delete(*args, **kwargs)

    class Meta(AbstractUser.Meta):
        pass
