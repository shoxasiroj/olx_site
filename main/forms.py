from django import forms
from django.contrib.auth import password_validation
from django.core.exceptions import ValidationError

from .apps import user_register
from .models import AdvUser


#Userni danniylarini o`zgartiradi
class ChangeUserForm(forms.ModelForm):
    email = forms.EmailField(required=True, label='Elektron pochta')

    class Meta:
        model = AdvUser
        fields = ('username', 'email', 'first_name', 'last_name', 'send_message')


# Registratsiya uchun forma
class RegisterUserForm(forms.ModelForm):
    email = forms.EmailField(required=True, label='Elektron pochta')
    password1 = forms.CharField(label='Parol',
                                widget=forms.PasswordInput,
                                help_text=password_validation.password_validators_help_text_html())
    password2 = forms.CharField(label='Takror parol',
                                widget=forms.PasswordInput,
                                help_text="Yuqoridagi parolni qaytarib tering")


    #password 8 ta raqamli va qiyin parol quyilganligini tekshiradi
    def clean_password1(self):
        password1 = self.cleaned_data['password1']
        try:
            password_validation.validate_password(password1, self.instance)
        except forms.ValidationError as error:
            self.add_error('password1', error)
        return password1


    def clean(self):
        super().clean()
        password1 = self.cleaned_data['password1']
        password2 = self.cleaned_data['password2']
        if password1 and password2 and password1 != password2:
            errors = {
                "password2": ValidationError(
                    "Sizning parolingiz bir biriga teng emas", code='password_mismatch'
                )
            }
            raise ValidationError(errors)


    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        user.is_active = True
        user.is_activated = True
        if commit:
            user.save()
        return user


# 2 ta parolni tekshiradi bir biriga tug`ri kelishini
    def clean(self):
        super().clean()
        password1 = self.cleaned_data['password1']
        password2 = self.cleaned_data['password2']
        if password1 and password2 and password1 != password2:
            errors = {
                "password2": ValidationError(
                    "Sizning parolingiz bir biriga tug`ri kelmadi", code='password_mismatch'
                )
            }
            raise ValidationError(errors)


    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        user.is_active = False
        user.is_activated = False
        if commit:
            user.save()
        user_register.send(RegisterUserForm, instance=user)
        return user


    class Meta:
        model = AdvUser
        fields = ('username', 'email', 'password1', 'password2', 'first_name', 'last_name', 'send_message')
