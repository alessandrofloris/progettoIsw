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
        newtrip_validation(form)
    else:
        form = TripForm()
    return newtrip_render(request, form)

def newtrip_render(request, form):
    return render(request, "travelGroup/newtrip.html", {"newTripForm": form})

def newtrip_validation(form):
    if form.is_valid:
        form.save()
        return HttpResponseRedirect("mytrips")
    else:
        return HttpResponse("not a valid form!")