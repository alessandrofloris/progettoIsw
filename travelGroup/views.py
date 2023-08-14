from django.http import HttpResponse

from .models import Trip
# Create your views here.

def index(request):
    return HttpResponse("Questa è la pagina principale!"
                        "Da questa pagina sarà possibile creare un nuovo gruppo di viaggio!")

def trips(request):
    trips = Trip.objects.all()
    output = ", ".join([t.name for t in trips])
    return HttpResponse(output)