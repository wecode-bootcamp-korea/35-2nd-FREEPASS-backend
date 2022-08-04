from django.urls import path 

from tickets.views import FlightLocationView, FlightScheduleList

urlpatterns = [
    path('/locations', FlightLocationView.as_view()),
    path('/schedules', FlightScheduleList.as_view())
]