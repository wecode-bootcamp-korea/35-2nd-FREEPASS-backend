import jwt

from django.test   import TestCase, Client
from unittest.mock import patch

from freepass import settings
from .models  import User

class KakaoSignInTest(TestCase):
    def setUp(self):
        User.objects.create(
            id           = 1,
            first_name   = "first",
            last_name    = "last",
            email        = "email@naver.com",
            phone_number = "010-0000-0000",
            birthday     = "2000-01-01",
            gender       = "male",
            kakao_id     = 1234
        )

    def tearDown(self):
        User.objects.all().delete()

    @patch("users.views.KakaoAPI.get_kakao_token")
    @patch("users.views.KakaoAPI.get_kakao_user")
    def test_kakao_signin_success_selet(self, mocked_user_info, mocked_access_token):
        client = Client()

        mocked_access_token.return_value = "access_token"
        mocked_user_info.return_value    = {
            'kakao_id': 1234,
            'email'   : 'email@naver.com',
            'gender'  : 'male'
        }
        headers = {"HTTP_Authorization" : "access_token"}

        response = client.get('/users/kakao', **headers, content_type="application/json")
        user     = User.objects.get(kakao_id=1234)
        token    = jwt.encode({'user_id':user.kakao_id}, settings.SECRET_KEY, settings.ALGORITHM)

        self.assertEqual(response.json(), 
            {
                'kakao_id': 1234,
                'created' : False,
                'token'   : token
            }
        )
        self.assertEqual(response.status_code, 200)

    @patch("users.views.KakaoAPI.get_kakao_token")
    @patch("users.views.KakaoAPI.get_kakao_user")
    def test_kakao_signin_success_create(self, mocked_user_info, mocked_access_token):
        client = Client()

        mocked_access_token.return_value = "access_token"
        mocked_user_info.return_value    = {
            'kakao_id': 4321,
            'email'   : 'example@naver.com',
            'gender'  : 'male'
        }
        headers = {"HTTP_Authorization" : "access_token"}

        response = client.get('/users/kakao', **headers, content_type="application/json")
        user     = User.objects.get(kakao_id=4321)
        token    = jwt.encode({'user_id':user.kakao_id}, settings.SECRET_KEY, settings.ALGORITHM)

        self.assertEqual(response.json(),
            {
                'kakao_id': 4321,
                'created' : True,
                'token'   : token
            }
        )
        self.assertEqual(response.status_code, 201)

    @patch("users.views.KakaoAPI.get_kakao_token")
    @patch("users.views.KakaoAPI.get_kakao_user")
    def test_kakao_signin_failure_keyerror(self, mocked_user_info, mocked_access_token):
        client = Client()

        mocked_access_token.return_value = "access_token"
        mocked_user_info.return_value    = {
            'kaka_id': 1234,
            'email'   : 'schk9611@naver.com',
            'gender'  : 'male'
        }
        headers = {"HTTP_Authorization" : "access_token"}

        response = client.get('/users/kakao', **headers, content_type="application/json")

        self.assertEqual(response.status_code, 400)