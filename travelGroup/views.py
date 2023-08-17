from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from .models import Trip
from .forms import TripForm

def index(request):
    return HttpResponse("This is the homepage! "
                        "From here you'll be able to create a new trip group!")


def trips(request):
    trip_list = Trip.objects.all()
    context = {
        "tripList": trip_list
    }
    return render(request, "travelGroup/trips.html", context)


def newtrip(request):
    if request.method == "POST":
        form = TripForm(request.POST)
        if form.is_valid:
            form.save()
            return HttpResponseRedirect("mytrips")  # Redirect alla pagina "trips"
    else:
        form = TripForm()
    return render(request, "travelGroup/newtrip.html", {"newTripForm": form})


def modify_trip(request, trip_id):
    return HttpResponse("You want to modify the trip %s." % trip_id)