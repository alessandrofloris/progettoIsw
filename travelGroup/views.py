from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from .models import Trip, CustomUser, Invitation, Comment, Activity
from .forms import TripForm, ActivityForm, RegistrationUserForm, AuthenticationForm, InvitationForm, CommentForm
from django.contrib.auth import login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.urls import reverse
from django.core.exceptions import ValidationError

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
                new_trip = form.save(commit=False)
                new_trip.save()
                new_trip.participants.add(request.user)
                new_trip.save()

                return HttpResponseRedirect(reverse('travelGroup:mytrips'))
            elif "create_add_button" in request.POST:
                new_trip = form.save(commit=False)
                new_trip.save()
                new_trip.participants.add(request.user)
                new_trip.save()
                url = "addactivity/" + str(new_trip.id)
                return HttpResponseRedirect(url)
    else:
        form = TripForm()
    return render(request, "travelGroup/newtrip.html", {"newTripForm": form})

def addactivity(request, trip_id):
    trip = get_object_or_404(Trip, id=trip_id)
    if request.method == "POST":
        form = ActivityForm(request.POST)
        form.trip = trip
        if form.is_valid():
            activity = form.save(commit=False)
            activity.trip = trip 
            activity.save()

            return HttpResponseRedirect(reverse('travelGroup:mytrips'))
    else:
        form = ActivityForm()
    return render(request, "travelGroup/addactivity.html", {"addActivityForm": form})

def modify_trip(request, trip_id):
    return HttpResponse("You want to modify the trip %s." % trip_id)

def invite(request):
    current_user = request.user

    # for testing purposes until the login is ready
    invitations_list = Invitation.objects.filter(recipient=current_user.email, state=False)

    if request.method == 'POST':
        form = InvitationForm(request.user, request.POST)

        if form.is_valid():
            sender_user = request.user
            recipient_email = form.cleaned_data['recipient_email']
            trip = form.cleaned_data['trip']

            try:
                invitation = Invitation.objects.create(sender=sender_user, recipient=recipient_email, trip=trip)
                invitation.save()
            except IntegrityError:
                return HttpResponse("You already made an identical invitation for this user")

            return HttpResponseRedirect("invite")

    else:
        form = InvitationForm(request.user)

    return render(request, 'travelGroup/invite.html', {'form': form, 'invitations_list': invitations_list})


def process_invitation(request, invitation_id):

    try:
        invitation = Invitation.objects.get(pk=invitation_id)

        if "accept" in request.POST:
            trip = invitation.trip
            user = request.user

            # Aggiungi l'utente come partecipante al viaggio
            trip.participants.add(user)

            # Imposta lo stato su True per accettare l'invito
            invitation.state = True
            invitation.save()

        if "decline" in request.POST:
            invitation.delete()

    except Invitation.DoesNotExist:
        pass

    return redirect('travelGroup:mytrips')


def view_trip(request, trip_id):

    comment_form = CommentForm()

    trip = Trip.objects.get(id=trip_id)
    participants = trip.participants.all()
    activities = trip.activity_set.all()
    comments = Comment.objects.filter(trip=trip)

    context = {
        "trip": trip,
        "participants": participants,
        "activities": activities,
        "comments": comments
    }
    # return render(request, "travelGroup/tripdetails.html", context)
    return render(request, "travelGroup/tripdetails.html", {"comment_form": comment_form, **context})

def add_comment(request, trip_id):
    current_user = request.user
    trip = Trip.objects.get(id=trip_id)

    if request.method == "POST":
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            content = comment_form.cleaned_data['content']
            new_comment = Comment.objects.create(content=content, user=current_user, trip=trip)
            new_comment.save()

    # Utilizza la funzione `redirect` per tornare alla pagina precedente
    return redirect(request.META.get('HTTP_REFERER', 'mytrips'))