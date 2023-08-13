from django.http import HttpResponse

# Create your views here.

def index(request):
    return HttpResponse("Questa è la pagina principale!"
                        "Da questa pagina sarà possibile creare un nuovo gruppo di viaggio!")
