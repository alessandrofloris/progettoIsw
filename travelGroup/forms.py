from django.forms import ModelForm, modelformset_factory
from .models import Trip, CustomUser, Activity, Invitation
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm


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
    exclude=(),
    widgets = {'start_date': CustomDateInput(), 'end_date': CustomDateInput()},
    extra=0)
