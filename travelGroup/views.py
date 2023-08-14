from django.http import HttpResponse
from django.shortcuts import render
from .models import Trip


def index(request):
    return HttpResponse("Questa è la pagina principale!"
                        "Da questa pagina sarà possibile creare un nuovo gruppo di viaggio!")


def trips(request):
    trip_list = Trip.objects.all()
    context = {
        "tripList": trip_list
    }
    return render(request, "travelGroup/trips.html", context)
