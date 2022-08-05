from django.http import JsonResponse
from django.views import View

from freepass import settings

class BookView(View):
    def get(self, request):
        


        result = {}

