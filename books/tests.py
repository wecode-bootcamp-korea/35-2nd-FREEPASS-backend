import jwt

from django.test import TestCase, Client

from tickets.models import Airline, Airplane, FlightInformation, Location
from users.models   import User
from freepass       import settings

class BookTest(TestCase):
    def setUp(self):
        Airline.objects.create(
            id   = 1,
            name = "항공",
            logo = "https://pixabay.com/ko/photos"
        )
        Airplane.objects.create(
            id         = 1,
            airline_id = 1,
            name       = "NAME001",
            code       = "code001"
        )
        Location.objects.bulk_create(
            [
                Location(id=1, name="김포", code="GMP"),
                Location(id=2, name="제주", code="CJU")
            ]
        )
        FlightInformation.objects.bulk_create(
            [
                FlightInformation(
                    id                       = 1,
                    departure_date           = "2022-08-13",
                    arrival_date             = "2022-08-13",
                    departure_time           = "10:00:00",
                    arrival_time             = "11:10:00",
                    normal_remaining_seats   = 10,
                    business_remaining_seats = 10,
                    price                    = 50000.00,
                    airplane_id              = 1,
                    arrival_location_id      = 2,
                    departure_location_id    = 1
                ),
                FlightInformation(
                    id                       = 2,
                    departure_date           = "2022-08-15",
                    arrival_date             = "2022-08-15",
                    departure_time           = "10:00:00",
                    arrival_time             = "11:10:00",
                    normal_remaining_seats   = 10,
                    business_remaining_seats = 10,
                    price                    = 50000.00,
                    airplane_id              = 1,
                    arrival_location_id      = 1,
                    departure_location_id    = 2
                )
            ]
        )
        User.objects.create(
            id           = 1,
            first_name   = "first",
            last_name    = "last",
            email        = "example@gmail.com",
            phone_number = "010-0000-0000",
            birthday     = "2000-01-01",
            gender       = "male",
            kakao_id     = 1234
        )
        self.token = jwt.encode({"id" : User.objects.get(id=1).id}, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

    def tearDown(self):
        Airline.objects.all().delete()
        Airplane.objects.all().delete()
        Location.objects.all().delete()
        User.objects.all().delete()
        FlightInformation.objects.all().delete()

    def test_bookview_get_success_oneway(self):
        client   = Client()
        headers  = {"HTTP_Authorization" : self.token}
        response = client.get("/books?flight_info_id=1&adult=1&seat_class=business", **headers, content_type="application/json")

        self.assertEqual(response.json(),
            {'result': 
                [
                    {
                        'date'              : '2022-08-13',
                        'airplane_code'     : 'code001',
                        'departure_time'    : '10:00:00',
                        'arrival_time'      : '11:10:00',
                        'departure_location': '김포',
                        'arrival_location'  : '제주',
                        'passenger_count'   : 1,
                        'remaining_seat'    : 10,
                        'total_price'       : 50000.0
                    }
                ]
            }
        )
        self.assertEqual(response.status_code, 200)


    def test_bookview_get_success_roundtrip(self):
        client   = Client()
        headers  = {"HTTP_Authorization" : self.token}
        response = client.get("/books?flight_info_id=1&flight_info_id=2&adult=1&seat_class=business", **headers, content_type="application/json")

        self.assertEqual(response.json(), 
            {'result': 
                [
                    {
                        'date'              : '2022-08-13',
                        'airplane_code'     : 'code001',
                        'departure_time'    : '10:00:00',
                        'arrival_time'      : '11:10:00',
                        'departure_location': '김포',
                        'arrival_location'  : '제주',
                        'passenger_count'   : 1,
                        'remaining_seat'    : 10,
                        'total_price'       : 50000.0
                    }, 
                    {
                        'date'              : '2022-08-15',
                        'airplane_code'     : 'code001',
                        'departure_time'    : '10:00:00',
                        'arrival_time'      : '11:10:00',
                        'departure_location': '제주',
                        'arrival_location'  : '김포',
                        'passenger_count'   : 1,
                        'remaining_seat'    : 10,
                        'total_price'       : 50000.0
                    }
                ]
            }
        )

        self.assertEqual(response.status_code, 200)