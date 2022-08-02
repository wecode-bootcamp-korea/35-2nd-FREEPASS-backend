from django.db import models

from core.models import TimeStampModel

class Book(TimeStampModel):
    ticketing      = models.ForeignKey('tickets.Ticketing', on_delete=models.CASCADE)
    user           = models.ForeignKey('users.User', on_delete=models.CASCADE)
    phone_number   = models.CharField(max_length=100)
    email          = models.CharField(max_length=100)
    first_name     = models.CharField(max_length=100)
    last_name      = models.CharField(max_length=100)
    booking_number = models.CharField(max_length=300)

    class Meta:
        db_table = 'books'

