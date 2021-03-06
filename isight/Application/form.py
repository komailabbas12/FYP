from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from .models import *

class RegisterUser(UserCreationForm):
    username = forms.CharField(label='pass',widget=forms.TextInput(attrs={'placeholder': '  Enter User Name','class':'form-control'}))
    password1 = forms.CharField(label='pass',widget=forms.PasswordInput(attrs={'placeholder': '  Enter Your Password','class':'form-control'}))
    password2 = forms.CharField(label='pass',widget=forms.PasswordInput(attrs={'placeholder': '  Confirm Password','class':'form-control'}))
    
    class Meta:
        model = User
        fields = ['username' , 'password1' , 'password2']


