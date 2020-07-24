from django.shortcuts import render
from django.http import HttpResponse,Http404,HttpResponseRedirect
from django.urls import reverse

from .models import Flight,Passenger

# Create your views here.
def index(request):
    context = {
        "flights":Flight.objects.all()
    }
    return render(request,"flights/index.html",context)

#with flight_id 
def flight(request,flight_id):
    try:
        flight = Flight.objects.get(pk=flight_id)
    except Flight.DoesNotExist:
        raise Http404("Flight not found")

    context = {
        "par":flight,
        "passengers":flight.passengers.all(),
        "non_passengers":Passenger.objects.exclude(flights=flight).all()
    }

    return render(request,"flights/flight.html",context)

def book(request,flight_id):
    try:
        passenger_id = int(request.POST["passenger"])
        passenger = Passenger.objects.get(pk=passenger_id)
        flight = Flight.objects.get(pk=flight_id)

    except KeyError:
        return render(request,"flights/error.html",{"message":"NO selection"})

    except passenger.DoesNotExist:
        return render(request,"flights/error.html",{"message":"No passenger"})

    except flight.DoesNotExist:
        return render(request,"flights/error.html",{"message":"No flights found"})
    
    passenger.flights.add(flight)

    return HttpResponseRedirect(reverse("flight",args=(flight_id,)))

    
    

    
