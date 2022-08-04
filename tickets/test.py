from django.test import TestCase, Client

from tickets.models import Airline, Airplane, FlightInformation, Location
from freepass       import settings

class LocationTest(TestCase) :
    def setUp(self):
        Location.objects.create(
            
            id        = 1,
            name      = "김포",
            code      = "GMP",
            latitude  = '37.3325',
            longitude = '126.4751',
        )

    def tearDown(self):
        Location.objects.all().delete()

    def test_location_search_view_get_success(self):
        client = Client()
        headers = {'HTTP_Authorization' : 'token'}
        response = client.get("/flights/locations?name=김포&code=GMP&latitude=37.3325&longitude=126.4751", **headers, content_type="application/json")

        self.assertEqual(response.json(),
            {'result': 
                [
                    {   
                        'id'        : 1,
                        'city_name' : "김포",
                        'code'      : "GMP",
                        'latitude'  : '37.3325',
                        'longitude' : '126.4751',
                    }
                ]
            }
        )            
        self.assertEqual(response.status_code, 200)           


class TicketTest(TestCase):
    maxDiff = None
    
    def setUp(self):
        Airline.objects.create(
            id = 1,
            name = 'test123',
            logo = "https://pixabay.com/ko/photos"
        )
        
        
        Airplane.objects.create(
            id = 1,
            airline_id =1,
            name = 'test',
            code = 'a123'
        )
        
        Location.objects.bulk_create (
            [Location(
                id = 1,
                name = "김포",
                code = "GMP",
                image = "https://pixabay.com/ko/photos",        
                latitude = '37.3325',
                longitude = '126.4751'),

            Location(
                id = 2,
                name = "제주",
                code = "CJU",
                image = "https://pixabay.com/ko/photos",
                latitude = '37.3325',
                longitude = '126.4751')
            ]
        )

        FlightInformation.objects.bulk_create (
            [
                FlightInformation(
                    id = 1,
                    airplane_id = 1,
                    departure_location_id = 1,
                    arrival_location_id =2,
                    departure_date = '2022-08-13',
                    arrival_date = '2022-08-13',
                    departure_time = '10:00:00',
                    arrival_time = '11:10:00',
                    normal_remaining_seats = 10,
                    business_remaining_seats = 10,
                    price = 50000.00
                ),
                
                FlightInformation(
                    id = 2,
                    airplane_id = 1,
                    departure_location_id = 2,
                    arrival_location_id = 1,
                    departure_date = '2022-08-15',
                    arrival_date = '2022-08-15',
                    departure_time = '20:00:00',
                    arrival_time = '21:10:00',
                    normal_remaining_seats = 10,
                    business_remaining_seats = 10,
                    price = 50000.00
                ) 
            ]
        )

    def tearDown(self):
        Airline.objects.all().delete()
        Airplane.objects.all().delete()
        Location.objects.all().delete()
        FlightInformation.objects.all().delete()
   
    def test_ticketview_get_success_one_way(self):
        client = Client()
        headers = {"HTTP_Authorization" : "token"}
        response = client.get("/flights/schedules?departure_location=김포&arrival_location=제주&departure_date=2022-08-13&adult=1&infant=2&remaining_seat=business&child=3&airlines=test123&",**headers, content_type="application/json")
 
        self.assertEqual(response.json(),
            {
                'location_result':
                    {
                        'departure_location': "김포",
                        'arrival_location'  : "제주",
                        'departure_date'    : ["2022-08-13"],
                        'adult'             : 1,
                        'infant'            : 2,
                        'child'             : 3,
                        'seat_class'        : "business",
                    },
                'one_way_result' : 
                    [
                        {   
                            "flight_id"              : 1,
                            "airline_id"             : 1,
                            "airline_name"           : "test123",
                            "airline_logo"           : "https://pixabay.com/ko/photos",
                            "airplane_id"            : 1,
                            "airplane_name"          : "test",
                            "airplane_code"          : "a123",
                            "departure_time"         : "10:00:00",
                            "arrival_time"           : "11:10:00",
                            'departure_location_name': "김포",
                            'arrival_location_name'  : "제주",
                            'departure_location_code': "GMP",
                            'arrival_location_code'  : "CJU",
                            'remaining_seat'         : 10,
                            'price'                  : '50000.000',
                            'total_price'            : 220000.0,
                            'passenger_count'        : 6      
                        }
                    ],    
                    
                'round_trip_result': [],    
                
            }
        )  
        self.assertEqual(response.status_code, 200)

    def test_ticketview_get_success_round_trip(self):
        client = Client()
        headers = {"HTTP_Authorization" : "token"}
        response = client.get("/flights/schedules?departure_location=제주&arrival_location=김포&departure_date=2022-08-13&departure_date=2022-08-15&adult=1&infant=2&remaining_seat=business&child=3&airlines=test123&ticket_type=round_trip",**headers, content_type="application/json")
        
        self.assertEqual(response.json(),
            {
                'location_result':
                    {
                        'departure_location': "제주",
                        'arrival_location'  : "김포",
                        'departure_date'    : ["2022-08-13", '2022-08-15'],
                        'adult'             : 1,
                        'infant'            : 2,
                        'child'             : 3,
                        'seat_class'        : "business",
                    },
                
                'one_way_result' : [],    
                
                    
                'round_trip_result': 
                    [ 
                        {   
                            "flight_id"              : 1,
                            "airline_id"             : 1,
                            "airline_name"           : "test123",
                            "airline_logo"           : "https://pixabay.com/ko/photos",
                            "airplane_id"            : 1,
                            "airplane_name"          : "test",
                            "airplane_code"          : "a123",
                            "departure_time"         : "10:00:00",
                            "arrival_time"           : "11:10:00",
                            'departure_location_name': "김포",
                            'arrival_location_name'  : "제주",
                            'departure_location_code': "GMP",
                            'arrival_location_code'  : "CJU",
                            'remaining_seat'         : 10,
                            'price'                  : '50000.000',
                            'total_price'            : 220000.0,
                            'passenger_count'        : 6      
                        }
                    ]    
                
            }
        )  
        self.assertEqual(response.status_code, 200)