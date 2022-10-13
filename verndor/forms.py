from django import forms
from .models import Vender


class VendorForm(forms.ModelForm):
    class Meta:
        model = Vender
        fields = ['vender_name','vender_license']