from django import forms

from apps.products.models import NewProductModel


class ProductForm(forms.ModelForm):
    excel_file = forms.FileField(required=False)

    class Meta:
        model = NewProductModel
        fields = '__all__'
