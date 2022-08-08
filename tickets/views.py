import json

from django.http      import JsonResponse
from django.views     import View
from django.db.models import Q

from tickets.models   import Ticketing, Airline, Airplane, Location , Discount
from tickets.models   import FlightInformation, SeatClass, Passenger, PassengerType, FlightDetail

class FlightLocationView(View):
    def get(self, request):
        locations = Location.objects.all()
    
        result = [{
                'id'        : location.id,
                'city_name' : location.name,
                'code'      : location.code,
                'latitude'  : location.latitude,
                'longitude' : location.longitude,

        } for location in locations]

        return JsonResponse({"result":result}, status=200)
        