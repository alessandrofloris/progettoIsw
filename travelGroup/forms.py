from django.forms import ModelForm, formset_factory
from .models import Trip, Activity

class TripForm(ModelForm):
    class Meta:
        model = Trip
        fields =  ["name", "destination", "departure_date", "arrival_date"]
        labels = {
            "name" : "Name",
            "destination" : "Destination",
            "departure_date" : "Departure Date",
            "arrival_date" : "Arrival Date"
        }

class ActivityForm(ModelForm):
    class Meta:
        model = Activity
        fields =  ["name", "description", "start_date", "end_date"]
        labels = {
            "name" : "Activity Name",
            "description" : "Activity Description",
            "start_date" : "Activity Start Date",
            "end_date" : "Activity End Date"
        }

ActivityFormSet = formset_factory(ActivityForm, extra=1)
