"""Forms for bookings + mock payment."""
from datetime import date
from django import forms
from .models import Booking, Payment


class BookingForm(forms.ModelForm):
    """Customer fills this in when booking a tour package."""

    class Meta:
        model = Booking
        fields = ['travel_date', 'num_travellers', 'special_requests']
        widgets = {
            'travel_date': forms.DateInput(attrs={
                'type': 'date',
                'class': 'future-only',
                'min': date.today().isoformat(),
            }),
            'special_requests': forms.Textarea(attrs={
                'rows': 3,
                'placeholder': 'Dietary needs, accessibility, etc.',
            }),
        }

    def __init__(self, *args, package=None, **kwargs):
        self.package = package
        super().__init__(*args, **kwargs)

    def clean_travel_date(self):
        travel_date = self.cleaned_data['travel_date']
        if travel_date < date.today():
            raise forms.ValidationError('Travel date cannot be in the past.')
        if self.package:
            if travel_date < self.package.available_from:
                raise forms.ValidationError(
                    f'This tour is only available from {self.package.available_from}.',
                )
            if travel_date > self.package.available_to:
                raise forms.ValidationError(
                    f'This tour is only available until {self.package.available_to}.',
                )
        return travel_date

    def clean_num_travellers(self):
        num = self.cleaned_data['num_travellers']
        if num < 1:
            raise forms.ValidationError('At least 1 traveller required.')
        if self.package and num > self.package.max_travellers:
            raise forms.ValidationError(
                f'Maximum {self.package.max_travellers} travellers per booking.',
            )
        return num


class BookingCustomizeForm(forms.ModelForm):
    """Customer can change travel date / traveller count on a pending booking."""
    class Meta:
        model = Booking
        fields = ['travel_date', 'num_travellers', 'special_requests']
        widgets = {
            'travel_date': forms.DateInput(attrs={'type': 'date'}),
            'special_requests': forms.Textarea(attrs={'rows': 3}),
        }


class PaymentForm(forms.Form):
    """
    Mock payment form — NO real card processing.
    Card number is just stored as the last 4 digits for display.
    """
    payment_method = forms.ChoiceField(
        choices=Payment.METHOD_CHOICES,
        widget=forms.RadioSelect,
        initial='card',
    )
    card_holder = forms.CharField(
        max_length=80,
        required=False,
        widget=forms.TextInput(attrs={'placeholder': 'Name as shown on card'}),
    )
    card_number = forms.CharField(
        max_length=23,  # 16 digits + 3 spaces, plus a buffer
        required=False,
        widget=forms.TextInput(attrs={
            'placeholder': '4242 4242 4242 4242',
            'id': 'id_card_number',
        }),
    )
    expiry = forms.CharField(
        max_length=5,
        required=False,
        widget=forms.TextInput(attrs={'placeholder': 'MM/YY'}),
    )
    cvv = forms.CharField(
        max_length=4,
        required=False,
        widget=forms.PasswordInput(attrs={'placeholder': '123'}),
    )

    def clean(self):
        cleaned = super().clean()
        method = cleaned.get('payment_method')
        if method == 'card':
            if not cleaned.get('card_holder'):
                self.add_error('card_holder', 'Required for card payment.')

            card_num = (cleaned.get('card_number') or '').replace(' ', '')
            if not card_num or len(card_num) < 13 or not card_num.isdigit():
                self.add_error('card_number', 'Please enter a valid card number.')

            if not cleaned.get('expiry'):
                self.add_error('expiry', 'Required.')
            if not cleaned.get('cvv'):
                self.add_error('cvv', 'Required.')
        return cleaned
