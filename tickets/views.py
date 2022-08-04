import json

from django.http           import JsonResponse
from django.views          import View
from django.db.models      import Q

from tickets.models        import Ticketing, Airline, Airplane, Location , Discount
from tickets.models        import FlightInformation, SeatClass, Passenger, PassengerType, FlightDetail
from core.views            import FindFlight

class FlightLocationView(View):
    def get(self, request):
        
        locations = Location.objects.all()
        result = [
            {
                'id'        : location.id,
                'city_name' : location.name,
                'code'      : location.code,
                'latitude'  : location.latitude,
                'longitude' : location.longitude,
                'image'     : location.image,

        } for location in locations]

        return JsonResponse({"result":result}, status=200)
        
class FlightScheduleList(View) :
    def get(self, request):
            # 모달
            departure_location = request.GET.get("departure_location")
            arrival_location   = request.GET.get("arrival_location")
            departure_date     = request.GET.getlist("departure_date")
            arrival_date       = request.GET.get("arrival_date")
            adult              = int(request.GET.get("adult", 0))
            infant             = int(request.GET.get("infant", 0))
            child              = int(request.GET.get("child", 0))
            seat_class         = request.GET.get("remaining_seat") # normal_remaining_seats / business_remaining_seats
            airlines           = request.GET.getlist('airlines')
            sort               = request.GET.get('sort', 'departure_time')
            ticket_type        = request.GET.get('ticket_type')
            passengers         = adult + infant + child
            CHILD_PRICE        = 0.8
            INFANT_PRICE       = 0.5
            findflight         = FindFlight(CHILD_PRICE, INFANT_PRICE)
            one_way_q          = Q()
            round_trip_q       = Q()
            round_trip         = []
            round_trip_result  = []
            
            if  departure_location :
                one_way_q &= Q(departure_location__name = departure_location)        
                round_trip_q &= Q(departure_location__name = arrival_location)
            
            if  arrival_location :
                one_way_q &= Q(arrival_location__name = arrival_location)
                round_trip_q &= Q(arrival_location__name = departure_location)
            
            if  departure_date :
                one_way_q &= Q(departure_date = departure_date[0])
                round_trip_q &= Q(departure_date__in = departure_date)
            
            if  seat_class == "business" :           
                total = int(adult) + int(infant) + int(child)
                one_way_q &= Q(business_remaining_seats__gte = total)
                round_trip_q &= Q(business_remaining_seats__gte = total)
                
            else:
                total = int(adult) + int(infant) + int(child)
                one_way_q &= Q(normal_remaining_seats__gte = total)
                round_trip_q &= Q(normal_remaining_seats__gte = total)

            if airlines : 
                one_way_q &= Q(airplane__airline__name__in = airlines)
                round_trip_q &= Q(airplane__airline__name__in = airlines)

            one_way = FlightInformation.objects.filter(one_way_q).order_by(sort).distinct()
            

            if ticket_type == "round_trip":

                round_trip = FlightInformation.objects.filter(round_trip_q).order_by(sort).distinct()
            
            #모달정보
            location_result = {
                
                'departure_location'        : departure_location,
                'arrival_location'          : arrival_location,
                'departure_date'            : departure_date,
                'adult'                     : adult,
                'infant'                    : infant,
                'child'                     : child,
                'seat_class'                : seat_class,

            }

            one_way_result = [ 
                {   
                    "flight_id"              : schedule.id,
                    "airline_id"             : schedule.airplane.airline.id,
                    "airline_name"           : schedule.airplane.airline.name,
                    "airline_logo"           : schedule.airplane.airline.logo,
                    "airplane_id"            : schedule.airplane.id,
                    "airplane_name"          : schedule.airplane.name,
                    "airplane_code"          : schedule.airplane.code,
                    "departure_time"         : schedule.departure_time,
                    "arrival_time"           : schedule.arrival_time,
                    'departure_location_name': schedule.departure_location.name,
                    'arrival_location_name'  : schedule.arrival_location.name,
                    'departure_location_code': schedule.departure_location.code,
                    'arrival_location_code'  : schedule.arrival_location.code,
                    'remaining_seat'         : findflight.seat_class(schedule, seat_class),
                    'price'                  : schedule.price,
                    'total_price'            : findflight.total_price(schedule, adult, child, infant),
                    'passenger_count'        : passengers                             
                } for schedule in one_way
            ]
           
            
            if  round_trip :
                round_trip_result = [
                {   
                        "flight_id"              : schedule.id,
                        "airline_id"             : schedule.airplane.airline.id,
                        "airline_name"           : schedule.airplane.airline.name,
                        "airline_logo"           : schedule.airplane.airline.logo,
                        "airplane_id"            : schedule.airplane.id,
                        "airplane_name"          : schedule.airplane.name,
                        "airplane_code"          : schedule.airplane.code,
                        "departure_time"         : schedule.departure_time,
                        "arrival_time"           : schedule.arrival_time,
                        'departure_location_name': schedule.departure_location.name,
                        'arrival_location_name'  : schedule.arrival_location.name,
                        'departure_location_code': schedule.departure_location.code,
                        'arrival_location_code'  : schedule.arrival_location.code,
                        'remaining_seat'         : findflight.seat_class(schedule, seat_class),
                        'price'                  : schedule.price,
                        'total_price'            : findflight.total_price(schedule, adult, child, infant),
                        'passenger_count'        : passengers                          
                } for schedule in round_trip
            ]

            return JsonResponse({'location_result':location_result, 'one_way_result' : one_way_result , 'round_trip_result': round_trip_result}, status=200)
