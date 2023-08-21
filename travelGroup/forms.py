from django.forms import ModelForm, modelformset_factory
from .models import Trip, CustomUser, Activity, Invitation
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm


class InvitationForm(forms.Form):
    class Meta:
        model = Invitation
        fields = ['recipient']

    recipient_email = forms.EmailField(label='Email')
    trip = forms.ModelChoiceField(queryset=Trip.objects.all(), label='Nome viaggio')


class RegistrationUserForm(UserCreationForm):
    class Meta(UserCreationForm):
        model = get_user_model()
        fields = ['username', 'first_name', 'last_name', 'email']
        labels = {
            "username" : "username",
            "first_name": "first_name",
            "last_name": "last_name",
            "email": "email",
        }


class TripForm(ModelForm):
    class Meta:
        model = Trip
        fields = '__all__'
        exclude = ['participants']  # Rimuovi completamente il campo participants dal form
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
