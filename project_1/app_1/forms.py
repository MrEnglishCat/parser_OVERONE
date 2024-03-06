from django import forms


class UpdateDataForm(forms.Form):
    description = forms.CharField()
    price = forms.IntegerField()
