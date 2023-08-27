from django.core.exceptions import ValidationError
from django.forms import ModelForm
from .models import Trip, CustomUser, Activity, Invitation
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.core.exceptions import ValidationError
from django.utils import timezone
from datetime import datetime, time


class InvitationForm(forms.Form):
    ERROR_EMAIL_NOT_FOUND = "Invitation not sent. Verify the inserted email"
    ERROR_INVITATION_EXISTS = "The user has already received an invitation for this trip"
    ERROR_ALREADY_PARTICIPATING = "The user is already in the trip group"

    recipient_email = forms.EmailField(label='Recipient email', required=True)
    trip = forms.ModelChoiceField(queryset=None, label='Trip name')

    def __init__(self, sender_user, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # current user
        self.user = sender_user

        # the method returns all the trips where the logged user is a partecipant
        self.fields['trip'].queryset = Trip.objects.filter(participants=self.user)

    def clean(self):
        cleaned_data = super().clean()

        # inputs from the form
        recipient_email = self.cleaned_data.get('recipient_email')
        selected_trip = self.cleaned_data.get('trip')

        # Verify the existence of the email in the system
        try:
            recipient = CustomUser.objects.get(email=recipient_email)
        except CustomUser.DoesNotExist:
            raise forms.ValidationError(self.ERROR_EMAIL_NOT_FOUND)

        # Verify if the recipient is already part of the trip group
        participants_emails = selected_trip.participants.values_list('email', flat=True)

        if recipient_email in participants_emails:
            raise forms.ValidationError(self.ERROR_ALREADY_PARTICIPATING)

        # Verify if the recipient has already received an identical invitation
        existing_invitation = Invitation.objects.filter(recipient=recipient_email, trip=selected_trip)

        if existing_invitation.exists():
            raise forms.ValidationError(self.ERROR_INVITATION_EXISTS)

        # return self.cleaned_data

class CommentForm(forms.Form):
    content = forms.CharField(widget=forms.Textarea)


class RegistrationUserForm(UserCreationForm):
    class Meta(UserCreationForm):
        model = CustomUser
        fields = ['username', 'first_name', 'last_name', 'email']
        labels = {
            "username": "username",
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

        if departure_date > arrival_date:
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

            if start_date >= end_date:
                raise ValidationError("Start date must be before the end date.")

        return cleaned_data
