from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render,redirect, get_object_or_404
from .models import Trip, User, Invitation, Activity
from .forms import TripForm, RegistrationUserForm, LoginUserForm, ActivityFormSet
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.urls import reverse


def login_page(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = authenticate(request, email=email, password=password)

        if user is not None:
            login(request, user)
            return redirect('trips')
        else:
            messages.info(request, 'email or password incorrect')

    context = {}
    return render(request, "travelGroup/login.html", context)


@login_required
def logout(request):
    logout(request)
    return redirect('loginPage')


def registration(request):
    form = RegistrationUserForm()
    if request.method == 'POST':
        form = RegistrationUserForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Account created')
    context = {'registrationUserForm': form}
    return render(request, "travelGroup/registration.html", context)


def index(request):
    return HttpResponse("This is the homepage! "
                        "From here you'll be able to create a new trip group!")


# @login_required
def trips(request):
    trip_list = Trip.objects.all()
    context = {
        "tripList": trip_list
    }
    return render(request, "travelGroup/trips.html", context)

# @login_required
def newtrip(request):
    if request.method == "POST":
        form = TripForm(request.POST)
        if form.is_valid:
            if "create_button" in request.POST:
                form.save()
                return HttpResponseRedirect(reverse('travelGroup:mytrips'))
            elif "create_add_button" in request.POST:
                new_trip = form.save()
                url = "addactivity/" + str(new_trip.id)
                return HttpResponseRedirect(url)
    else:
        form = TripForm()
    return render(request, "travelGroup/newtrip.html", {"newTripForm": form})

def addactivity(request, trip_id):
    trip = get_object_or_404(Trip, id=trip_id)

    if request.method == "POST":
        activity_formset = ActivityFormSet(request.POST, queryset=Activity.objects.filter(trip=trip))
        if activity_formset.is_valid():
            instances = activity_formset.save(commit=False)
            for instance in instances:
                instance.trip = trip
                instance.save()
            return HttpResponseRedirect(reverse('travelGroup:mytrips'))
    else:
        activity_formset = ActivityFormSet(queryset=Activity.objects.filter(trip=trip))
    return render(request, "travelGroup/addactivity.html", {"activity_formset": activity_formset})

def modify_trip(request, trip_id):
    return HttpResponse("You want to modify the trip %s." % trip_id)

def invite(request):
    user_list = User.objects.all()
    trip_list = Trip.objects.all()

    # for testing purposes until the login is ready
    invitation_list = get_user_invitations("topolino@gmail.com")
    # invitation_list = get_user_invitations("@gmail.com")

    context = {
        "users": user_list,
        "trips_list": trip_list,
        "invitations_list": invitation_list
    }

    return render(request, "travelGroup/invite.html", context)


def get_user_invitations(entered_email):
    try:
        invitation_list = Invitation.objects.filter(recipient=entered_email, state=False)
        return invitation_list
    except Invitation.DoesNotExist:
        return None
def invitation_form(request):
    if request.method == 'POST':
        sender_user = request.user   #Django's authentication
        recipient_email = request.POST.get('recipient_email')
        trip_id = request.POST.get('trip_id')  # id linked to the trip

        try:
            trip_instance = Trip.objects.get(id=trip_id)
            invitation = Invitation.objects.create(sender=sender_user, recipient=recipient_email, trip=trip_instance)
        except Trip.DoesNotExist:
            #   TODO
            # if the trip is chosen among the given options,
            # then it never happens
            pass
        except IntegrityError:
            #   TODO
            # When there's an identical invitation
            pass
        return HttpResponseRedirect("invite")


def view_trip(request, trip_id):

    trip = Trip.objects.get(id=trip_id)
    participants = trip.participants.all()
    activities = trip.activity_set.all()

    context = {
        "trip": trip,
        "participants": participants,
        "activities": activities
    }
    return render(request, "travelGroup/tripdetails.html", context)
