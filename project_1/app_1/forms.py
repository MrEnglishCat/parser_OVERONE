from django import forms
from django.contrib.auth.forms import UserChangeForm

class UpdateDataForm(forms.Form):
    description = forms.CharField(label='Описание:', widget=forms.Textarea(attrs={'rows':3, 'cols':70}))
    # price = forms.IntegerField(min_value=0, label='Цена')
    price = forms.FloatField(min_value=0, label='Цена')

