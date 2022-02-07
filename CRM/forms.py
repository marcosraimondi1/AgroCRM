from django import forms
from django.forms import ModelForm
from .models import User, Land, TenantProfile, Billing

# CREATE FORMS FROM MODELS


class landForm(ModelForm):
    class Meta:
        model = Land
        fields = ['title', 'description', 'hectares', 'location',
                  'map_link', 'lat', 'long', 'tenant']

    def __init__(self, *args, **kwargs):
        super(landForm, self).__init__(*args, **kwargs)
        # only show tenants related to this landlord
        if 'instance' in kwargs:
            self.fields['tenant'].queryset = TenantProfile.objects.filter(
                landlords=kwargs['instance'].landlord)

        self.fields['title'].widget.attrs.update({'class': 'form-control'})
        self.fields['description'].widget.attrs.update(
            {'class': 'form-control'})
        self.fields['hectares'].widget.attrs.update({'class': 'form-control'})
        self.fields['location'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': 'Country, State, City'})
        self.fields['map_link'].widget.attrs.update(
            {'class': 'form-control'})
        # self.fields['contract'].widget.attrs.update({'class': 'form-control'})
        self.fields['lat'].widget.attrs.update(
            {'class': 'form-control', 'min': -90, 'max': 90})
        self.fields['long'].widget.attrs.update(
            {'class': 'form-control', 'min': -180, 'max': 180})
        self.fields['tenant'].widget.attrs.update({'class': 'form-control'})


class DateInput(forms.DateInput):
    input_type = 'date'


class billingForm(ModelForm):
    class Meta:
        model = Billing
        fields = ['amount', 'method', 'period', 'payed']
        widgets = {
            'period': DateInput()
        }

    def __init__(self, *args, **kwargs):
        super(billingForm, self).__init__(*args, **kwargs)
        self.fields['amount'].widget.attrs.update(
            {'class': 'form-control', 'min': 0})
        self.fields['method'].widget.attrs.update({'class': 'form-control'})
        self.fields['period'].widget.attrs.update({'class': 'form-control'})
        self.fields['payed'].widget.attrs.update(
            {'class': 'form-control', 'min': 0})
