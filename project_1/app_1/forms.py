from django import forms
from django.contrib.auth.forms import UserChangeForm

class UpdateDataForm(forms.Form):
    description = forms.CharField(label='Описание:', widget=forms.Textarea(attrs={'rows':3, 'cols':70}))
    # price = forms.IntegerField(min_value=0, label='Цена')
    price = forms.FloatField(min_value=0, label='Цена')

class UserSettingsForm(UserChangeForm):
    first_name = forms.CharField(label='Имя', max_length=30)
    last_name = forms.CharField(label='Фамилия', max_length=30)
    email = forms.CharField(label='e-mail', max_length=75)

