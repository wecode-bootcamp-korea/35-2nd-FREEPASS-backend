from django.urls import path, include

urlpatterns = [
    path('flights', include('tickets.urls')),
    path('users', include('users.urls')),
    path('books', include('books.urls'))
]
