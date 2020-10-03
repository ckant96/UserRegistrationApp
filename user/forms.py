from django import forms
from django.contrib.auth.models import User
from .models import UserProfile

class Userform(forms.ModelForm):
    username =forms.CharField(label='',widget= forms.TextInput(attrs={'placeholder': 'Username'}))
    password = forms.CharField(label='', widget=forms.PasswordInput(attrs={'placeholder': 'Password'}))
    class Meta:
        model=User
        fields=('username','password')