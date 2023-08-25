from .models import SuperCategory, ChildCategory
from django import forms


class ChildCategoryForm(forms.ModelForm):
    parent_category = forms.ModelChoiceField(queryset=SuperCategory.objects.all(),
                                             empty_label=None,
                                             label='Ota Categoriya', required=True)

    class Meta:
        model = ChildCategory
        fields = '__all__'
