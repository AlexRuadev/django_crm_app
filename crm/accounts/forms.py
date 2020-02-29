# Creating a form the python way
from django.forms import ModelForm
from .models import Order


class OrderForm(ModelForm):
    class Meta:
        # Minimum 2 fields
        model = Order
        fields = '__all__'
