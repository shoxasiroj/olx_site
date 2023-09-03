from django import forms
from captcha.fields import CaptchaField
from .models import Comment


# Login qilgan userlar uchun forma Comment
class UserCommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        exclude = ('is_active',)
        widgets = {'elon': forms.HiddenInput}


# Login qilmagan foydalanuvchilar uchunn forms Comment
class GuestCommentForm(forms.ModelForm):
    captcha = CaptchaField(label='Rasmdagi matnni kiriting', error_messages={'invalid': 'Notug`ri kiritdingiz'})

    class Meta:
        model = Comment
        exclude = ('is_active',)
        widgets = {'elon': forms.HiddenInput}
