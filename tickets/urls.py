from django.urls import path 

from tickets.views import FlightLocationView

urlpatterns = [
    path('/locations', FlightLocationView.as_view()),
]