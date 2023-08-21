from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from .models import Trip, CustomUser, Invitation
from .forms import TripForm, ActivityFormSet, RegistrationUserForm, AuthenticationForm, InvitationForm
from django.contrib.auth import login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.conf import settings


def login_page(request):
    form = AuthenticationForm()
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('/mytrips')
        else:
            messages.info(request, 'email or password incorrect')

    context = {'authenticationForm': form}
    return render(request, "travelGroup/login.html", context)


@login_required()
def logout_page(request):
    logout(request)
    return redirect(settings.LOGIN_REDIRECT_URL)


def registration(request):
    form = RegistrationUserForm()
    if request.method == 'POST':
        form = RegistrationUserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(settings.LOGIN_REDIRECT_URL)

    context = {'registrationUserForm': form}
    return render(request, "travelGroup/registration.html", context)


@login_required()
def trips(request):
    trip_list = Trip.objects.filter(participants=request.user)
    context = {
        "tripList": trip_list
    }
    return render(request, "travelGroup/trips.html", context)


def newtrip(request):
    if request.method == "POST":
        form = TripForm(request.POST)
        if form.is_valid():
            if "create_button" in request.POST:
                trip = form.save(commit=False)
                trip.save()
                trip.participants.add(request.user)
                trip.save()

                return HttpResponseRedirect("mytrips")
            elif "create_add_button" in request.POST:
                form.save()
                return HttpResponseRedirect("addactivity")
    else:
        form = TripForm()
    return render(request, "travelGroup/newtrip.html", {"newTripForm": form})

def modify_trip(request, trip_id):
    return HttpResponse("You want to modify the trip %s." % trip_id)

def addactivity(request):
    if request.method == "POST":
        activity_formset = ActivityFormSet(request.POST)
        if activity_formset.is_valid:
            activity_formset.save()
            return HttpResponseRedirect("mytrips")  # Redirect alla pagina "mytrips"
    else:
        activity_formset = ActivityFormSet()
    return render(request, "travelGroup/addactivity.html", {"activity_formset": activity_formset})



def invite(request):
    current_user = request.user

    # for testing purposes until the login is ready
    invitations_list = Invitation.objects.filter(recipient=current_user.email, state=False)

    if request.method == 'POST':
        form = InvitationForm(request.POST)
        if form.is_valid():
            sender_user = request.user
            recipient_email = form.cleaned_data['recipient_email']
            trip = form.cleaned_data['trip']

            try:
                invitation = Invitation.objects.create(sender=sender_user, recipient=recipient_email, trip=trip)
                invitation.save()
            except IntegrityError:
                return HttpResponse("You already made an identical invitation for this user")

            return HttpResponseRedirect("invite")  # Reindirizza l'utente a una pagina di conferma

    else:
        form = InvitationForm()

    return render(request, 'travelGroup/invite.html', {'form': form, 'invitations_list': invitations_list})

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
