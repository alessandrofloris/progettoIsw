from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render,redirect
from .models import Trip, CustomUser, Invitation
from .forms import TripForm, ActivityFormSet, UserCreationForm, AuthenticationForm
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
    form = UserCreationForm()
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(settings.LOGIN_REDIRECT_URL)

    context = {'userCreationForm': form}
    return render(request, "travelGroup/registration.html", context)


@login_required()
def trips(request):
    trip_list = Trip.objects.all()
    context = {
        "tripList": trip_list
    }
    return render(request, "travelGroup/trips.html", context)


@login_required()
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
    context = {"newTripForm": newtrip_form, "activity_formset": activity_formset}
    return render(request, "travelGroup/newtrip.html", context)


def newtrip_validation(form):
    if form.is_valid():
        return HttpResponseRedirect("mytrips")
    else:
        return HttpResponse("not a valid form!")


def modify_trip(request, trip_id):
    return HttpResponse("You want to modify the trip %s." % trip_id)


def addactivity_validation(form):
    if form.is_valid():
        form.save()
        # HttpResponseRedirect to newtrip
        return HttpResponse("ok")
    else:
        return HttpResponse("not a valid form!")


def invite(request):
    user_list = CustomUser.objects.all()
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
