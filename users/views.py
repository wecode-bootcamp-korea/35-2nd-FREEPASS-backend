import requests
import jwt

from django.http  import JsonResponse
from django.views import View
from users.models import User

from freepass import settings

class KakaoAPI:
    def __init__(self, KAKAO_APP_KEY, REDIRECT_URI):
        self.kakao_app_key = KAKAO_APP_KEY
        self.redirect_uri  = REDIRECT_URI

    def get_kakao_token(self, auth_code):
        data = {
            "grant_type"  : "authorization_code",
            "client_id"   : self.kakao_app_key,
            "redirect_uri": self.redirect_uri,
            "code"        : auth_code
        }
        response     = requests.post("https://kauth.kakao.com/oauth/token", data=data, timeout=3)
        access_token = response.json()['access_token']
        return access_token

    def get_kakao_user(self, kakao_token):
        kakao_headers = {"Authorization" : f"Bearer ${kakao_token}"}
        response      = requests.get("https://kapi.kakao.com/v2/user/me", headers=kakao_headers, timeout=3)
        kakao_user    = response.json()
        user_info     = {
            "kakao_id": kakao_user['id'],
            "email"   : kakao_user["kakao_account"]['email'],
            "gender"  : kakao_user["kakao_account"]['gender']
        }
        return user_info


class KakaoCallbackView(View):
    def get(self, request):
        try:
            auth_code   = request.GET.get('code')
            kakao_api   = KakaoAPI(settings.KAKAO_APP_KEY, settings.REDIRECT_URI)
            kakao_token = kakao_api.get_kakao_token(auth_code)
            kakao_user  = kakao_api.get_kakao_user(kakao_token)

            user, is_created = User.objects.get_or_create(
                kakao_id = kakao_user['kakao_id'],
                defaults = {
                    'email'   : kakao_user['email'],
                    'gender'  : kakao_user['gender'],
                    'kakao_id': kakao_user['kakao_id']
                }
            )

            status_code = 201 if is_created else 200

            access_token = jwt.encode({"user_id":user.kakao_id}, settings.SECRET_KEY, settings.ALGORITHM)

            return JsonResponse({'kakao_id': user.kakao_id, 'created': is_created, 'token': access_token}, status=status_code)

        except KeyError:
            return JsonResponse({'message' : 'KEY_ERROR'}, status=400)
