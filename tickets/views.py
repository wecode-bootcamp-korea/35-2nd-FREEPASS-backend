from django.http      import JsonResponse
from django.views     import View

from tickets.models   import Location

class FlightLocationView(View):
    def get(self, request):
        locations = Location.objects.all()
        result = [
            {
                'id'        : location.id,
                'city_name' : location.name,
                'code'      : location.code,
                'latitude'  : location.latitude,
                'longitude' : location.longitude,
                'image'     : location.image,

        } for location in locations]

        return JsonResponse({"result":result}, status=200)
