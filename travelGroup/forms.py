from django.forms import ModelForm
from .models import Trip

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
