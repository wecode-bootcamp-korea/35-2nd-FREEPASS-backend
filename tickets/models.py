from django.db import models

class Airline(models.Model):
    name = models.CharField(max_length=100)
    logo = models.URLField(max_length=600)

    class Meta:
        db_table = 'airlines'

class Airplane(models.Model):
    airline = models.ForeignKey('Airline', on_delete=models.CASCADE)
    name    = models.CharField(max_length=100)
    code    = models.CharField(max_length=100)

    class Meta:
        db_table = 'airplanes'

class Location(models.Model):
    name      = models.CharField(max_length=100)
    code      = models.CharField(max_length=100)
    image     = models.URLField(max_length=600, null=True)
    latitude  = models.CharField(max_length=100, null=True)
    longitude = models.CharField(max_length=100, null=True)

    class Meta:
        db_table = 'locations'

class FlightInformation(models.Model):
    airplane                 = models.ForeignKey('Airplane', on_delete=models.CASCADE)
    departure_location       = models.ForeignKey('Location', on_delete=models.CASCADE, related_name='departure_flight_informations')
    arrival_location         = models.ForeignKey('Location', on_delete=models.CASCADE, related_name='arrival_flight_informations')
    departure_date           = models.DateField()
    arrival_date             = models.DateField()
    departure_time           = models.TimeField()
    arrival_time             = models.TimeField()
    normal_remaining_seats   = models.IntegerField()
    business_remaining_seats = models.IntegerField()
    price                    = models.DecimalField(decimal_places=3, max_digits=10)

    class Meta:
        db_table = 'flight_informations'

class SeatClass(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        db_table = 'seat_classes'

class PassengerType(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        db_table = 'passenger_types'

class Discount(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        db_table = 'discounts'

class FlightDetail(models.Model):
    flight_information = models.ForeignKey('FlightInformation', on_delete=models.CASCADE)
    seat_class         = models.ForeignKey('SeatClass', on_delete=models.CASCADE)
    passenger_type     = models.ForeignKey('PassengerType', on_delete=models.CASCADE)
    discount           = models.ForeignKey('Discount', on_delete=models.CASCADE)

    class Meta:
        db_table = 'flight_details'

class Passenger(models.Model):
    first_name = models.CharField(max_length=100)
    last_name  = models.CharField(max_length=100)
    birthday   = models.DateField()
    gender     = models.CharField(max_length=100)
    country    = models.CharField(max_length=100)

    class Meta:
        db_table = 'passengers'

class Ticketing(models.Model): 
    flight_detail = models.ForeignKey('FlightDetail', on_delete=models.CASCADE)
    passenger     = models.ForeignKey('Passenger', on_delete=models.CASCADE)
    ticket_number = models.CharField(max_length=300)

    class Meta:
        db_table = 'ticketings'