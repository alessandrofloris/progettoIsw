from django.forms import ModelForm
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

        # the method returns all the trips where the logged user is a partecipant
        trips = Trip.objects.filter(participants=user)

        # new field to choose a trip
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
        exclude = ['participants']
        widgets = {
            'departure_date': forms.DateInput(attrs={'type': 'date'}),
            'arrival_date': forms.DateInput(attrs={'type': 'date'}),
        }

class ActivityForm(ModelForm):
    class Meta:
        model = Activity
        fields = '__all__'
        exclude = ['trip']
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
        }
