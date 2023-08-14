from django.http import HttpResponse
from django.shortcuts import render
from django.template import loader
from .models import Trip

# Create your views here.

def index(request):
    return HttpResponse("Questa è la pagina principale!"
                        "Da questa pagina sarà possibile creare un nuovo gruppo di viaggio!")

def trips(request):
    trips = Trip.objects.all()
    context = {
        "tripList": trips
    }
    return render(request, "travelGroup/trips.html", context)
