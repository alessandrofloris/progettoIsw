from django.forms import ModelForm, modelformset_factory
from .models import Trip, CustomUser, Activity, Invitation
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm


class InvitationForm(forms.Form):
    recipient_email = forms.EmailField(label='Email', widget=forms.EmailInput(attrs={'placeholder': 'Email'}))
    trip = forms.ModelChoiceField(queryset=None, label='Nome viaggio')

    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Ottieni tutti i viaggi in cui l'utente loggato è un partecipante
        trips = Trip.objects.filter(participants=user)

        # Crea un campo di scelta per i viaggi
        self.fields['trip'].queryset = trips

class CommentForm(forms.Form):
    content = forms.CharField(widget=forms.Textarea)

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
