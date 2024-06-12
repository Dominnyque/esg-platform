import stripe
from django.conf import settings
from django.contrib.auth.models import User
from django.views.generic import TemplateView, View, ListView
from django.views.generic.edit import CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views.generic.edit import FormView
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from .forms import SignUpForm, CarForm, TransportationForm, TransportationFlightForm, FlightForm, TransportationBoatForm, BoatForm, CarbonFootprintForm, OffsetByAmountForm
from django.contrib.auth import login
from django.utils.decorators import method_decorator
from .models import Offset, Transportation, TransportationFlight, Flight, Event



class SignUpView(CreateView):
    model = User
    form_class = SignUpForm
    template_name = 'registration/signup.html'
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        response = super().form_valid(form)
        user = form.save()
        login(self.request, user)
        return response








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
                cost_in_euro_multiplier = cost_in_euro * 15
                amount_in_cents = int(cost_in_euro_multiplier * 100)  # Amount in cents

                # Render payment page with Stripe button
                return render(
                    self.request,
                    'payment.html',
                    {
                        'cost_in_euro': cost_in_euro,
                        'cost_in_euro_multiplier': cost_in_euro_multiplier,
                        'amount_in_cents': amount_in_cents,
                        'stripe_public_key': settings.STRIPE_PUBLIC_KEY
                    },
                )

        # Handle form validation errors
        return render(self.request, self.template_name, {'car_form': car_form, 'transportation_form': transportation})

    def calculate_carbon_emission(self, car_type, distance, distance_type):
        emission_factors = {
            'small_car': 0.0001743,
            'luxury_car': 0.00032797,
            'suv': 0.00021844,
            'van': 0.0001912,
            'hybrid_car': 0.00012,
            'motorcycle': 0.0001136,
        }

        multiplier = 1 if distance_type == 'km' else 7.7900747
        return emission_factors[car_type] * distance * multiplier







stripe.api_key = settings.STRIPE_SECRET_KEY

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
                    flight_form.cleaned_data['flight_class'],
                    transportation.cleaned_data['flight_hours'],
                    transportation.cleaned_data['distance_in'],
                    transportation.cleaned_data['travelers']
                )

                transportation_instance.flight_hours = transportation.cleaned_data['flight_hours']

                transportation_instance.save()

                # Calculate cost in Euro (€) based on carbon emission (1€ per metric ton)
                cost_in_euro = transportation_instance.carbon_emission
                cost_in_euro_multiplier = cost_in_euro * 15
                amount_in_cents = int(cost_in_euro_multiplier * 100)  # Amount in cents

                # Render payment page with Stripe button
                return render(
                    self.request,
                    'payment.html',
                    {
                        'cost_in_euro': cost_in_euro,
                        'cost_in_euro_multiplier': cost_in_euro_multiplier,
                        'amount_in_cents': amount_in_cents,
                        'stripe_public_key': settings.STRIPE_PUBLIC_KEY
                    },
                )

        # Handle form validation errors
        return render(self.request, self.template_name, {'flight_form': flight_form, 'transportation_form': transportation})

    def calculate_carbon_emission(self, flight_class, flight_hours, distance_in, travelers):
        emission_factors = {
            'economy': 0.1875,
            'premium': 0.27333,
        }
        multiplier = 1 if distance_in == 'hour' else 7.7
        return emission_factors[flight_class] * flight_hours * multiplier * travelers









stripe.api_key = settings.STRIPE_SECRET_KEY
class StripeCheckoutView(View):
    def post(self, request, *args, **kwargs):
        token = request.POST.get('stripeToken')
        amount_in_cents = int(request.POST.get('amount_in_cents'))

        try:
            charge = stripe.Charge.create(
                amount=amount_in_cents,
                currency='eur',
                description='Carbon Offset',
                source=token
            )
            offset = Offset.objects.create(
                user = self.request.user,
                offset_amount = amount_in_cents / 100,
                metric_tone = round(amount_in_cents / 1500, 2)

            )
            return render(request, 'success.html', {'charge': charge})

        except stripe.error.CardError as e:
            # The card has been declined
            return render(request, 'payment.html', {
                'error': f"Card error: {e.user_message}",
                'stripe_public_key': settings.STRIPE_PUBLIC_KEY,
                'amount_in_cents': amount_in_cents
            })
        except stripe.error.RateLimitError as e:
            # Too many requests made to the API too quickly
            return render(request, 'payment.html', {
                'error': "Rate limit error, please try again.",
                'stripe_public_key': settings.STRIPE_PUBLIC_KEY,
                'amount_in_cents': amount_in_cents
            })
        except stripe.error.InvalidRequestError as e:
            # Invalid parameters were supplied to Stripe's API
            return render(request, 'payment.html', {
                'error': "Invalid request error.",
                'stripe_public_key': settings.STRIPE_PUBLIC_KEY,
                'amount_in_cents': amount_in_cents
            })
        except stripe.error.AuthenticationError as e:
            # Authentication with Stripe's API failed
            return render(request, 'payment.html', {
                'error': "Authentication error, please try again.",
                'stripe_public_key': settings.STRIPE_PUBLIC_KEY,
                'amount_in_cents': amount_in_cents
            })
        except stripe.error.APIConnectionError as e:
            # Network communication with Stripe failed
            return render(request, 'payment.html', {
                'error': "Network error, please try again.",
                'stripe_public_key': settings.STRIPE_PUBLIC_KEY,
                'amount_in_cents': amount_in_cents
            })
        except stripe.error.StripeError as e:
            # Display a generic error to the user, and maybe send
            # yourself an email
            return render(request, 'payment.html', {
                'error': "Something went wrong. Please try again.",
                'stripe_public_key': settings.STRIPE_PUBLIC_KEY,
                'amount_in_cents': amount_in_cents
            })
        except Exception as e:
            # Something else happened, completely unrelated to Stripe
            return render(request, 'payment.html', {
                'error': f"An error occurred: {str(e)}",
                'stripe_public_key': settings.STRIPE_PUBLIC_KEY,
                'amount_in_cents': amount_in_cents
            })





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
                cost_in_euro_multiplier = cost_in_euro * 15
                amount_in_cents = int(cost_in_euro_multiplier * 100)  # Amount in cents

                # Render payment page with Stripe button
                return render(
                    self.request,
                    'payment.html',
                    {
                        'cost_in_euro': cost_in_euro,
                        'cost_in_euro_multiplier': cost_in_euro_multiplier,
                        'amount_in_cents': amount_in_cents,
                        'stripe_public_key': settings.STRIPE_PUBLIC_KEY
                    },
                )

        # Handle form validation errors
        return render(self.request, self.template_name, {'boat_form': boat_form, 'transportation_form': transportation})

    def calculate_carbon_emission(self, boat_type, days, people):
        emission_factors = {
            'cruise': 0.29266,
            'live_aboard': 0.56066,
        }
        multiplier = 1
        return emission_factors[boat_type] * days * people * multiplier







class CalculateCarbonOffsetView(TemplateView):
    template_name = 'calculate_offset.html'
    success_url = reverse_lazy('payment_page')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = CarbonFootprintForm()
        return context

    def post(self, request, *args, **kwargs):
        form = CarbonFootprintForm(request.POST)
        if form.is_valid():
            carbon_footprint = form.cleaned_data['carbon_footprint']
            # Assuming 1 Euro per metric ton
            cost_in_euro = carbon_footprint
            cost_in_euro_multiplier = cost_in_euro * 15  # Converting to cents for Stripe
            amount_in_cents = int(cost_in_euro_multiplier * 100)  # Amount in cents

            # Render payment page with Stripe button
            return render(
                self.request,
                'payment.html',
                {
                    'cost_in_euro': cost_in_euro,
                    'cost_in_euro_multiplier': cost_in_euro_multiplier,
                    'amount_in_cents': amount_in_cents,
                    'stripe_public_key': settings.STRIPE_PUBLIC_KEY
                }
            )
        else:
            return render(request, self.template_name, {'form': form})




class CarbonOffsetByAmountView(TemplateView):
    template_name = 'offset_by_amount.html'
    success_url = reverse_lazy('payment_page')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = OffsetByAmountForm()
        return context

    def post(self, request, *args, **kwargs):
        form = OffsetByAmountForm(request.POST)
        if form.is_valid():
            footprint_offset = form.cleaned_data['footprint_offset'] / 15
            # Assuming 1 Euro per metric ton
            cost_in_euro = footprint_offset
            cost_in_euro_multiplier = cost_in_euro * 15  # Converting to cents for Stripe
            amount_in_cents = int(cost_in_euro_multiplier * 100)  # Amount in cents

            # Render payment page with Stripe button
            return render(
                self.request,
                'payment.html',
                {
                    'cost_in_euro': cost_in_euro,
                    'cost_in_euro_multiplier': cost_in_euro_multiplier,
                    'amount_in_cents': amount_in_cents,
                    'stripe_public_key': settings.STRIPE_PUBLIC_KEY
                }
            )
        else:
            return render(request, self.template_name, {'form': form})


@method_decorator(login_required, name='dispatch')
class MyProfileView(LoginRequiredMixin, ListView):
    model = Offset
    template_name = 'my_profile.html'
    context_object_name = 'offsets'

    def get_queryset(self):
        return Offset.objects.filter(user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = self.request.user
        return context