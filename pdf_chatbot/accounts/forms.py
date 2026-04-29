from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import CustomUser


class RegisterForm(UserCreationForm):
    phone_number = forms.CharField(
        max_length=17,
        help_text='Enter your phone number (e.g. +919876543210)',
        widget=forms.TextInput(attrs={'placeholder': '+91XXXXXXXXXX'})
    )
    email = forms.EmailField(
        required=False,
        widget=forms.EmailInput(attrs={'placeholder': 'email@example.com (optional)'})
    )

    class Meta:
        model = CustomUser
        fields = ['username', 'phone_number', 'email', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['placeholder'] = 'Choose a username'
        self.fields['password1'].widget.attrs['placeholder'] = 'Create a password'
        self.fields['password2'].widget.attrs['placeholder'] = 'Confirm password'
        for field in self.fields.values():
            field.widget.attrs['autocomplete'] = 'off'


class LoginForm(AuthenticationForm):
    username = forms.CharField(
        label='Username',
        widget=forms.TextInput(attrs={'placeholder': 'Your username', 'autofocus': True})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Your password'})
    )
