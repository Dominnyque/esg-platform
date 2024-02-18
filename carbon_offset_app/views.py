# carbon_offset_app/views.py
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views.generic.edit import FormView
from django.urls import reverse_lazy
from .forms import CarForm, TransportationForm, TransportationFlightForm, FlightForm, TransportationBoatForm, BoatForm
from .models import Transportation, TransportationFlight, Flight, Event

class CalculateCarbonOffsetCarView(FormView):
    template_name = 'calculate_car.html'
    form_class = CarForm
    form_class_transportation = TransportationForm
    success_url = reverse_lazy('payment_page')

    def get(self, request, *args, **kwargs):
        car_form = self.form_class()
        transportation_form = self.form_class_transportation()
        return render(self.request, self.template_name, {'car_form': car_form, 'transportation_form': transportation_form})

    def form_valid(self, form):
        car_form = self.form_class(self.request.POST)
        if car_form.is_valid():
            transportation = self.form_class_transportation(self.request.POST)
            if transportation.is_valid():
                transportation_instance = transportation.save(commit=False)

                # If user is authenticated, use their user instance
                if self.request.user.is_authenticated:
                    transportation_instance.user = self.request.user
                else:
                    # For guest users, create a temporary user (you may customize this logic)
                    temporary_user, created = User.objects.get_or_create(username='guest_user')
                    transportation_instance.user = temporary_user

                # Calculate carbon emission based on the selected car type, distance, and distance type
                transportation_instance.carbon_emission = self.calculate_carbon_emission(
                    car_form.cleaned_data['car_type'],
                    transportation.cleaned_data['distance'],
                    transportation.cleaned_data['distance_type']
                )

                transportation_instance.distance = transportation.cleaned_data['distance']

                transportation_instance.save()

                # Calculate cost in Euro (€) based on carbon emission (1€ per metric ton)
                cost_in_euro = transportation_instance.carbon_emission
                cost_in_euro_multiplier = cost_in_euro * 2
                return render(
                    self.request,
                    'payment.html',
                    {'cost_in_euro': cost_in_euro, 'cost_in_euro_multiplier': cost_in_euro_multiplier, 'stripe_public_key': 'your_stripe_public_key'},
                    )


        # Handle form validation errors
        return render(self.request, self.template_name, {'car_form': car_form, 'transportation_form': transportation})

    def calculate_carbon_emission(self, car_type, distance, distance_type):
        emission_factors = {
            'small_car': 0.2,
            'luxury_car': 0.5,
            'suv': 0.4,
            'van': 0.4,
            'hybrid_car': 0.2,
            'motorcycle': 0.1,
        }

        multiplier = 0.13 if distance_type == 'hour' else 0.6
        return emission_factors[car_type] * distance * multiplier


class CalculateCarbonOffsetFlightView(FormView):
    template_name = 'calculate_flight.html'
    form_class = FlightForm
    form_class_transportation = TransportationFlightForm
    success_url = reverse_lazy('payment_page')

    def get(self, request, *args, **kwargs):
        flight_form = self.form_class()
        transportation_form = self.form_class_transportation()
        return render(self.request, self.template_name, {'flight_form': flight_form, 'transportation_form': transportation_form})

    def form_valid(self, form):
        flight_form = self.form_class(self.request.POST)
        if flight_form.is_valid():
            transportation = self.form_class_transportation(self.request.POST)
            if transportation.is_valid():
                transportation_instance = transportation.save(commit=False)

                # Set the event based on the selected value
                event_id = transportation.cleaned_data['event']
                transportation_instance.event_id = event_id

                # If user is authenticated, use their user instance
                if self.request.user.is_authenticated:
                    transportation_instance.user = self.request.user
                else:
                    # For guest users, create a temporary user (you may customize this logic)
                    temporary_user, created = User.objects.get_or_create(username='guest_user')
                    transportation_instance.user = temporary_user

                # Calculate carbon emission based on the selected car type, distance, and distance type
                transportation_instance.carbon_emission = self.calculate_carbon_emission(
                    flight_form.cleaned_data['flight_type'],
                    transportation.cleaned_data['distance'],
                    transportation.cleaned_data['distance_type']
                )

                transportation_instance.distance = transportation.cleaned_data['distance']

                transportation_instance.save()

                # Calculate cost in Euro (€) based on carbon emission (1€ per metric ton)
                cost_in_euro = transportation_instance.carbon_emission
                cost_in_euro_multiplier = cost_in_euro * 2
                return render(
                    self.request,
                    'payment.html',
                    {'cost_in_euro': cost_in_euro, 'cost_in_euro_multiplier': cost_in_euro_multiplier, 'stripe_public_key': 'your_stripe_public_key'},
                    )


        # Handle form validation errors
        return render(self.request, self.template_name, {'flight_form': flight_form, 'transportation_form': transportation})

    def calculate_carbon_emission(self, flight_type, distance, distance_type):
        emission_factors = {
            'economy': 0.6,
            'premium': 0.9,
        }
        multiplier = 0.13 if distance_type == 'hour' else 0.6
        return emission_factors[flight_type] * distance * multiplier


class CalculateCarbonOffsetBoatView(FormView):
    template_name = 'calculate_boat.html'
    form_class = BoatForm
    form_class_transportation = TransportationBoatForm
    success_url = reverse_lazy('payment_page')

    def get(self, request, *args, **kwargs):
        boat_form = self.form_class()
        transportation_form = self.form_class_transportation()
        return render(self.request, self.template_name, {'boat_form': boat_form, 'transportation_form': transportation_form})

    def form_valid(self, form):
        boat_form = self.form_class(self.request.POST)
        if boat_form.is_valid():
            transportation = self.form_class_transportation(self.request.POST)
            if transportation.is_valid():
                transportation_instance = transportation.save(commit=False)

                # If user is authenticated, use their user instance
                if self.request.user.is_authenticated:
                    transportation_instance.user = self.request.user
                else:
                    # For guest users, create a temporary user (you may customize this logic)
                    temporary_user, created = User.objects.get_or_create(username='guest_user')
                    transportation_instance.user = temporary_user

                # Calculate carbon emission based on the selected car type, distance, and distance type
                transportation_instance.carbon_emission = self.calculate_carbon_emission(
                    boat_form.cleaned_data['boat_type'],
                    transportation.cleaned_data['days'],
                    transportation.cleaned_data['people']
                )

                transportation_instance.days = transportation.cleaned_data['days']
                transportation_instance.people = transportation.cleaned_data['people']

                transportation_instance.save()

                # Calculate cost in Euro (€) based on carbon emission (1€ per metric ton)
                cost_in_euro = transportation_instance.carbon_emission
                cost_in_euro_multiplier = cost_in_euro * 2
                return render(
                    self.request,
                    'payment.html',
                    {'cost_in_euro': cost_in_euro, 'cost_in_euro_multiplier': cost_in_euro_multiplier, 'stripe_public_key': 'your_stripe_public_key'},
                    )


        # Handle form validation errors
        return render(self.request, self.template_name, {'boat_form': boat_form, 'transportation_form': transportation})

    def calculate_carbon_emission(self, boat_type, days, people):
        emission_factors = {
            'cruise': 0.5,
            'live_aboard': 1.4,
        }
        multiplier = 0.13 #if distance_type == 'hour' else 0.6
        return emission_factors[boat_type] * days *people *multiplier