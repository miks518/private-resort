from django import forms
from django.core.exceptions import ValidationError
from datetime import date
from .models import Reservation


class ReservationForm(forms.ModelForm):
    """Form for creating a new reservation (Process 2.2)."""

    check_in = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-input'}),
    )
    check_out = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-input'}),
    )

    class Meta:
        model = Reservation
        fields = ['check_in', 'check_out', 'guests', 'special_requests']
        widgets = {
            'guests': forms.NumberInput(attrs={'class': 'form-input', 'min': 1}),
            'special_requests': forms.Textarea(attrs={
                'class': 'form-input', 'rows': 3,
                'placeholder': 'Any special requests or notes...',
            }),
        }

    def clean(self):
        cleaned_data = super().clean()
        check_in = cleaned_data.get('check_in')
        check_out = cleaned_data.get('check_out')

        if check_in and check_out:
            if check_in < date.today():
                raise ValidationError('Check-in date cannot be in the past.')
            if check_out <= check_in:
                raise ValidationError('Check-out date must be after check-in date.')

        return cleaned_data

    def clean_guests(self):
        guests = self.cleaned_data.get('guests')
        if guests and guests < 1:
            raise ValidationError('At least 1 guest is required.')
        return guests
