# carbon_offset_app/forms.py
from django import forms
from .models import Transportation, TransportationFlight, TransportationBoat, Car, Flight, Event

class CarForm(forms.Form):
    car_type = forms.ChoiceField(choices=[
        ('small_car', 'Small Car'),
        ('luxury_car', 'Luxury Car'),
        ('suv', 'SUV'),
        ('van', 'Van'),
        ('hybrid_car', 'Hybrid Car'),
        ('motorcycle', 'Motorcycle'),
    ])

class TransportationForm(forms.ModelForm):
    distance = forms.FloatField()
    distance_type = forms.ChoiceField(choices=[
        ('hour', 'Hour'),
        ('km', 'Kilometer'),
    ])

    class Meta:
        model = Transportation
        fields = ['car']  # Include 'car' here temporarily
        widgets = {
            'car': forms.HiddenInput(),  # Hide 'car' field
        }

class FlightForm(forms.Form):
    flight_type = forms.ChoiceField(choices=[
        ('economy', 'Economy'),
        ('premium', 'Premium'),
    ])

class TransportationFlightForm(forms.ModelForm):
    distance = forms.FloatField()
    distance_type = forms.ChoiceField(choices=[
        ('hour', 'Hour'),
        ('km', 'Kilometer'),
    ])
    event = forms.ModelChoiceField(queryset=Event.objects.all(), empty_label=None)

    class Meta:
        model = TransportationFlight
        fields = ['event', 'distance_type', 'distance', 'flight']
        widgets = {
            'flight': forms.HiddenInput(),
        }

class BoatForm(forms.Form):
    boat_type = forms.ChoiceField(choices=[
        ('cruise', 'Cruise'),
        ('live_aboard', 'Live aboard'),
    ])

class TransportationBoatForm(forms.ModelForm):
    days = forms.FloatField()
    people = forms.FloatField()

    class Meta:
        model = TransportationBoat
        fields = ['boat']  # Include 'boat' here temporarily
        widgets = {
            'boat': forms.HiddenInput(),  # Hide 'boat' field
        }

class PaymentForm(forms.Form):
    card_number = forms.CharField(label='Card Number', max_length=16, widget=forms.TextInput(attrs={'placeholder': 'Enter your card number'}))
    exp_date = forms.CharField(label='Expiration Date', max_length=5, widget=forms.TextInput(attrs={'placeholder': 'MM/YY'}))
    cvc = forms.CharField(label='CVC', max_length=3, widget=forms.TextInput(attrs={'placeholder': 'CVC'}))
    name_on_card = forms.CharField(label='Name on Card', max_length=255, widget=forms.TextInput(attrs={'placeholder': 'Enter the name on your card'}))

    def clean_card_number(self):
        card_number = self.cleaned_data.get('card_number')
        if not card_number.isdigit() or len(card_number) != 16:
            raise forms.ValidationError('Invalid card number. Please enter a 16-digit card number.')
        return card_number

    def clean_exp_date(self):
        exp_date = self.cleaned_data.get('exp_date')
        if not exp_date or len(exp_date) != 5 or not exp_date[:2].isdigit() or not exp_date[3:].isdigit() or exp_date[2] != '/':
            raise forms.ValidationError('Invalid expiration date. Please enter the expiration date in MM/YY format.')
        return exp_date

    def clean_cvc(self):
        cvc = self.cleaned_data.get('cvc')
        if not cvc.isdigit() or len(cvc) != 3:
            raise forms.ValidationError('Invalid CVC. Please enter a 3-digit CVC.')
        return cvc
