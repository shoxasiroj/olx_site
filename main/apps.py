from django.apps import AppConfig
from django.dispatch import Signal
from .utilities import sent_activation_letter

user_register = Signal()


# Registratsiyadan o`tgan odamlar uchun emailga silka boradi
def user_register_dispatcher(sender, **kwargs):
    sent_activation_letter(kwargs['instance'])


user_register.connect(user_register_dispatcher)


class MainConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'main'
