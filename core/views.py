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