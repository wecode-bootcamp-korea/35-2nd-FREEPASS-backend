import jwt
from django.http  import JsonResponse

from users.models import User
from freepass     import settings

def signin_decorator(func):
    def wrapper(self, request, *args, **kwargs):
        try:
            access_token = request.headers.get('Authorization')
            payload      = jwt.decode(access_token, settings.SECRET_KEY, algorithms=settings.ALGORITHM)
            user         = User.objects.get(kakao_id=payload['user_id'])
            request.user = user

            return func(self, request, *args, **kwargs)

        except jwt.exceptions.DecodeError:
            return JsonResponse({'message' : 'INVALID_TOKEN'}, status=401)
        except User.DoesNotExist:
            return JsonResponse({'message' : 'INVALID_TOKEN'}, settings=401)

    return wrapper

class FindFlight:
    def __init__(self, CHILD_PRICE, INFANT_PRICE):
        self.child_price  = CHILD_PRICE
        self.infant_price = INFANT_PRICE

    def seat_class(self, flight, seat_class):
        remaining_seat = {
            "normal"  : flight.normal_remaining_seats,
            "business": flight.business_remaining_seats
        }
        return remaining_seat.get(seat_class)

    def total_price(self, flight, adult, child, infant):
        adult_price  = adult * int(flight.price)
        child_price  = (child * int(flight.price)) * self.child_price
        infant_price = (infant * int(flight.price)) * self.infant_price
        return adult_price + child_price + infant_price
