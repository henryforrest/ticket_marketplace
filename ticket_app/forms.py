from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from datetime import datetime

from .models import UserProfile, UserProfile


class LoginForm(forms.Form):
    username = forms.CharField(max_length=50)
    password = forms.CharField(
        max_length=50,
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Password',  # Optional: Customize the placeholder text
        })
    )


class SignUpForm(UserCreationForm):
    class Meta:
        model = UserProfile
        fields = ['username', 'email', 'password1', 'password2',]

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not email.endswith('@exeter.ac.uk'):
            raise forms.ValidationError('You must have an exeter univerity email to register')
        return email
    


class SellTicketForm(forms.Form):
    event = forms.CharField(
        max_length=50, 
        widget=forms.TextInput(attrs={'placeholder': 'Venue'}))
    date = forms.DateField(
        initial=datetime.today,
        widget=forms.DateInput(attrs={'type': 'date'}))
    time = forms.TimeField(
        initial='7:00',
        widget=forms.TimeInput(attrs={'type': 'time', 'step': 1800 })
    )
    price = forms.DecimalField(
        initial=5,
        min_value=1.00,  # Ensures price is at least 0.01
        max_digits=10, 
        decimal_places=2,
        widget=forms.NumberInput(attrs={'step': '0.50', 'placeholder': 'Enter price (e.g. 19.99)'})
    )


class edit_profile(forms.Form):
    username = forms.CharField(label='Change Username', max_length=100)
    email = forms.EmailField(label='Change Email')
    