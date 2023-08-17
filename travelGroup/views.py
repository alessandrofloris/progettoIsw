from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from .models import Trip
from .forms import TripForm, RegistrationUserForm, LoginUserForm


def login(request):
    form = LoginUserForm()
    if request.method == 'POST':
        form = LoginUserForm(request.POST)
        if form.is_valid():
            form.save()
    context = {'loginUserForm': form}
    return render(request, "travelGroup/login.html", context)


def registration(request):
    form = RegistrationUserForm()
    if request.method == 'POST':
        form = RegistrationUserForm(request.POST)
        if form.is_valid():
            form.save()
    context = {'registrationUserForm': form}
    return render(request, "travelGroup/registration.html", context)


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
