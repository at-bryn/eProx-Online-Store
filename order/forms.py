from django import forms
from .models import *


class OrderCreateForm(forms.ModelForm):
    class Meta:
        model = Checkout
        fields = "__all__"


class CheckoutForm(forms.ModelForm):
    class Meta:
        model = Checkout
        fields = ('first_name','last_name','email','address')
