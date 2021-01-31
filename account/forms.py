from django import forms
from django.contrib.auth.forms import UserCreationForm
from account.models import User
from django.contrib.auth.forms import PasswordChangeForm


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
        model = User
        fields = ["username", "email"]


class LoginForm(forms.Form):
    username = forms.CharField(label='Username', max_length=100,
                               widget=forms.TextInput(attrs={'class': "form-control"}), required=True)
    password = forms.CharField(label='Password', max_length=100,
                               widget=forms.PasswordInput(attrs={'class': "form-control"}), required=True)


class ChangePasswordForm(PasswordChangeForm):
    old_password = forms.CharField(label='Current password', max_length=100,
                                   widget=forms.PasswordInput(attrs={'class': "form-control saddlebrown__input"}),
                                   required=True)
    new_password1 = forms.CharField(label='New password', max_length=100,
                                    widget=forms.PasswordInput(attrs={'class': "form-control saddlebrown__input"}),
                                    required=True)
    new_password2 = forms.CharField(label='Confirm new password', max_length=100,
                                    widget=forms.PasswordInput(attrs={'class': "form-control saddlebrown__input"}),
                                    required=True)
