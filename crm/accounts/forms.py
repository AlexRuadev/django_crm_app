# Creating a form the python way
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms

from .models import *


class CustomerForm(ModelForm):
    class Meta:
        model = Customer
        Formfields = '__all__'
        exclude = ['user']


class OrderForm(ModelForm):
    class Meta:
        # Minimum 2 fields
        model = Order
        fields = '__all__'


class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
