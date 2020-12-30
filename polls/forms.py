from django import forms
from django.contrib.auth.models import User


class LoginForm(forms.Form):
    required_css_class = 'form-control'
    username = forms.CharField(label="username", max_length=100, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'username'}))
    password = forms.CharField(label="password", max_length=100, widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'password'}))


class RegisterForm(forms.ModelForm):
    username = forms.CharField(label="username", max_length=100, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'username'}))
    password = forms.CharField(label="password", max_length=100, widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'password'}))
    email = forms.CharField(label="email", widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'email'}))
    first_name = forms.CharField(label="firstname", max_length=100, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'firstname'}))
    last_name = forms.CharField(label="lastname", max_length=100, widget=forms.TextInput(attrs={'class': 'form-control','placeholder': 'lastname'}))

    class Meta:
        model = User
        fields = ['username', 'password', 'email', 'first_name', 'last_name']
