# carbon_offset_app/urls.py
from django.urls import path
from .views import CalculateCarbonOffsetCarView, CalculateCarbonOffsetFlightView, CalculateCarbonOffsetBoatView

urlpatterns = [
    path('calculate/car/', CalculateCarbonOffsetCarView.as_view(), name='calculate_car'),
    path('calculate/flight/', CalculateCarbonOffsetFlightView.as_view(), name='calculate_flight'),
    path('calculate/boat/', CalculateCarbonOffsetBoatView.as_view(), name='calculate_boat'),
    # Add other URLs for flight, boat, and payment as needed
]
