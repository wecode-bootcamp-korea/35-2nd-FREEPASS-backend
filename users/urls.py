from django.urls import path
from users.views import KakaoCallbackView

urlpatterns = [
    path('/kakao', KakaoCallbackView.as_view())
]