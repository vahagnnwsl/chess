from django import forms
from django.contrib.auth.forms import UserCreationForm
from player.models import Player


class RegisterForm(UserCreationForm):
    email = forms.CharField(label='Email', max_length=100, widget=forms.EmailInput(attrs={'class': "form-control"}),
                            required=True)
    username = forms.CharField(label='Username', max_length=100,
                               widget=forms.TextInput(attrs={'class': "form-control"}), required=True)
    password1 = forms.CharField(label='Password', max_length=100,
                                widget=forms.PasswordInput(attrs={'class': "form-control"}), required=True)
    password2 = forms.CharField(label='Password', max_length=100,
                                widget=forms.PasswordInput(attrs={'class': "form-control"}), required=True)

    class Meta:
        model = Player
        fields = ["username", "email"]


class LoginForm(forms.Form):
    username = forms.CharField(label='Username', max_length=100,
                               widget=forms.TextInput(attrs={'class': "form-control"}), required=True)
    password = forms.CharField(label='Password', max_length=100,
                               widget=forms.PasswordInput(attrs={'class': "form-control"}), required=True)
