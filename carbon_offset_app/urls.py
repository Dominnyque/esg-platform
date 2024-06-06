# carbon_offset_app/urls.py
from django.urls import path
from .views import(
    CalculateCarbonOffsetCarView,
    CalculateCarbonOffsetFlightView,
    CalculateCarbonOffsetBoatView,
    CalculateCarbonOffsetView,
    CarbonOffsetByAmountView

)

urlpatterns = [
    path('calculate/car/', CalculateCarbonOffsetCarView.as_view(), name='calculate_car'),
    path('calculate/flight/', CalculateCarbonOffsetFlightView.as_view(), name='calculate_flight'),
    path('calculate/boat/', CalculateCarbonOffsetBoatView.as_view(), name='calculate_boat'),
    path('calculate/', CalculateCarbonOffsetView.as_view(), name='calculate_offset'),
    path('offset-amount/', CarbonOffsetByAmountView.as_view(), name='offset_amount'),
]
