from django.http import JsonResponse
from django.views import View

from freepass import settings

from tickets.models import FlightInformation

class BookView(View):
    def get(self, request):
        flight_info_id = request.GET.getlist('flight_info_id')
        adult = int(request.GET.get('adult', 0))
        infant = int(request.GET.get('infant', 0))
        child = int(request.GET.get('child', 0))
        seat_class = request.GET.get('seat_class')

        # print(flight_info_id)
        flights = [ FlightInformation.objects.get(id=id) for id in flight_info_id ]
        # print(flight)

        passengers = adult + infant + child

        def business(flight):
            if seat_class=="normal":
                return flight.normal_remaining_seats
            else:
                return flight.business_remaining_seats

        def total_price(flight):
            adult_price = adult * int(flight.price)
            infant_price = (infant * int(flight.price)) * 0.8
            child_price = (child * int(flight.price)) * 0.5
            return adult_price + infant_price + child_price

        result = [
            {
                "date"              : flight.departure_date,
                "airplane_code"     : flight.airplane.code,
                "departure_time"    : flight.departure_time,
                "arrival_time"      : flight.arrival_time,
                "departure_location": flight.departure_location.name,
                "arrival_location"  : flight.arrival_location.name,
                "passenger_count"  : passengers,
                "remaining_seat" : business(flight),
                "total_price"       : total_price(flight) 
            } for flight in flights
        ]
        print(result)

        return JsonResponse({'message' : result})