from django.forms import ModelForm
from .models import Trip, CustomUser, Activity, Invitation
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.core.exceptions import ValidationError
from django.utils import timezone
from datetime import datetime, time


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

    def clean(self):
        cleaned_data = super().clean()
        departure_date = cleaned_data.get('departure_date')
        arrival_date = cleaned_data.get('arrival_date')

        if departure_date and arrival_date and departure_date >= arrival_date:
            raise ValidationError("Departure date must be before the arrival date.")

        return cleaned_data

class ActivityForm(ModelForm):
    class Meta:
        model = Activity
        fields = '__all__'
        exclude = ['trip']
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
        }
    
    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get('start_date')
        end_date = cleaned_data.get('end_date')

        if start_date and end_date:
            trip = self.trip
            trip_start_date = timezone.make_aware(datetime.combine(trip.departure_date, time.min))
            trip_end_date = timezone.make_aware(datetime.combine(trip.arrival_date, time.max))

            if start_date < trip_start_date or end_date > trip_end_date:
                raise ValidationError("Activity dates must be within the trip dates range.")

            if start_date and end_date and start_date >= end_date:
                raise ValidationError("Start date must be before the end date.")

        return cleaned_data
