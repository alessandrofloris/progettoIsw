from django.forms import ModelForm, modelformset_factory
from .models import Trip, CustomUser, Activity, Invitation
from django.contrib.auth.forms import UserCreationForm
from django import forms


class RegistrationUserForm(ModelForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'first_name', 'last_name', 'email', 'password']
        labels = {
            "username": "username",
            "first_name": "first_name",
            "last_name": "last_name",
            "email": "email",
            "password": "password"
        }


class LoginUserForm(ModelForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'password']
        labels = {
            "username": "email",
            "password": "password"
        }


class TripForm(ModelForm):
    class Meta:
        model = Trip
        fields = '__all__'
        widgets = {
            'departure_date': forms.DateInput(attrs={'type': 'date'}),
            'arrival_date': forms.DateInput(attrs={'type': 'date'}),
        }


class CustomDateInput(forms.DateInput):
    input_type = 'date'


ActivityFormSet = modelformset_factory(
    Activity, 
    exclude=('trip',),
    widgets = {'start_date': CustomDateInput(), 'end_date': CustomDateInput()},
    extra=0)
