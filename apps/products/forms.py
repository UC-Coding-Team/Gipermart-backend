from django import forms

from apps.products.models import NewProductModel


class ProductForm(forms.ModelForm):
    excel_file = forms.FileField()

    class Meta:
        model = NewProductModel
        fields = '__all__'
