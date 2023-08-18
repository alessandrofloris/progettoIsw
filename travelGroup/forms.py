from django.forms import ModelForm, modelformset_factory
from .models import Trip, User, Activity
from django.contrib.auth.forms import UserCreationForm
from django import forms

class RegistrationUserForm(ModelForm):
    class Meta:
        model = User
        fields = ['name', 'surname', 'email', 'password']
        labels = {
            "name": "name",
            "surname": "surname",
            "email": "email",
            "password": "password"
        }

class LoginUserForm(ModelForm):
    class Meta:
        model = User
        fields = ['email', 'password']
        labels = {
            "email": "email",
            "password": "password"
        }

class TripForm(ModelForm):
    class Meta:
        model = Trip
        fields = ["name", "destination", "departure_date", "arrival_date"]

ActivityFormSet = modelformset_factory(Activity, exclude=())
