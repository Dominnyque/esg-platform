# carbon_offset_app/urls.py
from django.urls import path
from .views import CalculateCarbonOffsetCarView

urlpatterns = [
    path('calculate/car/', CalculateCarbonOffsetCarView.as_view(), name='calculate_car'),
    # Add other URLs for flight, boat, and payment as needed
]
