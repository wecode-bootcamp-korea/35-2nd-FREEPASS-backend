from django.http  import JsonResponse
from django.views import View

from tickets.models import FlightInformation
from core.views     import FindFlight

class BookView(View):
    def get(self, request):
        try:
            flight_information_id = request.GET.getlist('flight_info_id')
            adult                 = int(request.GET.get('adult', 0))
            child                 = int(request.GET.get('child', 0))
            infant                = int(request.GET.get('infant', 0))
            seat_class            = request.GET.get('seat_class')
            passengers            = adult + child + infant
            flights               = [FlightInformation.objects.get(id=id) for id in flight_information_id]
            CHILD_PRICE           = 0.8
            INFANT_PRICE          = 0.5
            findflight            = FindFlight(CHILD_PRICE, INFANT_PRICE)

            result = [
                {
                    "date"              : flight.departure_date,
                    "airplane_code"     : flight.airplane.code,
                    "departure_time"    : flight.departure_time,
                    "arrival_time"      : flight.arrival_time,
                    "departure_location": flight.departure_location.name,
                    "arrival_location"  : flight.arrival_location.name,
                    "passenger_count"   : passengers,
                    "remaining_seat"    : findflight.seat_class(flight, seat_class),
                    "total_price"       : findflight.total_price(flight, adult, child, infant)
                } for flight in flights
            ]

            return JsonResponse({'result' : result}, status=200)

        except FlightInformation.DoesNotExist:
            return JsonResponse({'message' : 'DOES_NOT_EXIST'})