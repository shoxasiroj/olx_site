from django import forms
from elon.models import Elon, AdditionalImage

class SearchForm(forms.Form):
    keyword = forms.CharField(required=False, max_length=20, label='')


class ElonCreateForm(forms.ModelForm):
    class Meta:
        model = Elon
        fields = '__all__'
        widgets = {'author': forms.HiddenInput}


AdditionalImageFormSet = forms.inlineformset_factory(Elon, AdditionalImage, fields='__all__')
