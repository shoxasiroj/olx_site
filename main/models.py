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


from django.db.models.signals import post_save
from comment.models import Comment
from main.utilities import sent_comment_notification


# Comment saqlanganda emailga xabar jo`natish uchun funksiya
def post_save_dispatcher(sender, **kwargs):
    print("post-saveeeeeee")
    author = kwargs['instance'].elon.author
    if kwargs['created'] and author.send_message:
        print("authooooooooooor", author)
        sent_comment_notification(kwargs['instance'])


post_save.connect(post_save_dispatcher, sender=Comment)
