from dataclasses import field
from django import forms
from .models import *


class PaymentForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = ['amount','email']
        widgets = {
            'amount': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
        }
