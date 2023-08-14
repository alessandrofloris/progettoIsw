from django.http import HttpResponse
from django.shortcuts import render
from .models import Trip
from .forms import TripForm

def index(request):
    return HttpResponse("This is the homepage! "
                        "From here you'll be able to create a new trip group!")


def trips(request):
    trip_list = Trip.objects.all()
    # the context is a dictionary mapping template 
    # variable names to Python objects.
    # the string "tripList" is the dictionary's key 
    # and the associated value refers to the "trips.html" file 
    # placed into "travelGroup/templates/travelGroup" path.
    context = {
        "tripList": trip_list
    }
    return render(request, "travelGroup/trips.html", context)

def newtrip(request):
    if request.method == "POST":
        form = TripForm(request.POST)
        if form.is_valid:
            form.save()
            return redirect("mytrips")  # Redirect alla pagina "trips"
    else:
        form = TripForm()
    return render(request, "travelGroup/newtrip.html", {"newTripForm": form})
