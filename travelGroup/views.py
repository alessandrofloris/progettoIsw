from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from .models import Trip, User
from .forms import TripForm, ActivityFormSet, RegistrationUserForm, LoginUserForm


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
        newtrip_form = TripForm(request.POST)
        activity_formset = ActivityFormSet(request.POST)
        newtrip_validation(newtrip_form)
        # activity validation
    else:
        newtrip_form = TripForm()
        activity_formset = ActivityFormSet()
    return newtrip_render(request, newtrip_form, activity_formset)


def newtrip_render(request, newtrip_form, activity_formset):
    return render(request, "travelGroup/newtrip.html", {"newTripForm": newtrip_form, "activity_formset": activity_formset})


def modify_trip(request, trip_id):
    return HttpResponse("You want to modify the trip %s." % trip_id)


def newtrip_validation(form):
    if form.is_valid:
        form.save()
        return HttpResponseRedirect("mytrips")
    else:
        return HttpResponse("not a valid form!")


def addactivity_validation(form):
    if form.is_valid:
        form.save()
        # HttpResponseRedirect to newtrip
        return HttpResponse("ok")
    else:
        return HttpResponse("not a valid form!")


def invite(request):
    user_list = User.objects.all()
    trip_list = Trip.objects.all()

    context = {
        "users": user_list,
        "tripList": trip_list
    }

    return render(request, "travelGroup/invite.html", context)


def view_trip(request, trip_id):

    trip = Trip.objects.get(id=trip_id)
    partecipants = trip.participants.all()
    context = {
        "trip": trip,
        "partecipants": partecipants
    }
    return render(request, "travelGroup/tripdetails.html", context)