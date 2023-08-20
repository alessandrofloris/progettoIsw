from django.forms import ModelForm, modelformset_factory
from .models import Trip, CustomUser, Activity, Invitation
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm


class RegistrationUserForm(UserCreationForm):
    class Meta(UserCreationForm):
        model = get_user_model()
        fields = ['username', 'first_name', 'last_name', 'email']
        labels = {
            "username": "username",
            "name": "name",
            "surname": "surname",
            "first_name": "first_name",
            "last_name": "last_name",
            "email": "email",
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
