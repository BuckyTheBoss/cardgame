from django import forms
from .models import *


class OfferForm(forms.ModelForm):
    class Meta:
        model = Offer
        fields = ['card']
        widgets = {
            'card': forms.Select(attrs={'class':'form-control col-6 d-inline mx-2'})
        }
        labels = {
            'card': 'Pokemon'
        }
