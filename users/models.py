from django.db import models

from core.models import TimeStampModel

class User(TimeStampModel):
    first_name   = models.CharField(max_length=100, null=True)
    last_name    = models.CharField(max_length=100, null=True)
    email        = models.CharField(max_length=200, unique=True, null=True)
    phone_number = models.CharField(max_length=200, null=True)
    birthday     = models.DateField(null=True)
    gender       = models.CharField(max_length=100, null=True)
    kakao_id     = models.BigIntegerField()

    class Meta:
        db_table = 'users'
