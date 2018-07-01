from django import forms
from .models import *

#Login Form
class LoginForm(forms.Form):
    username=forms.CharField(
        max_length=20,
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username', 'required': 'true'})
    )
    password=forms.CharField(
        max_length=20,
        required=True,
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password', 'required': 'true'})
    )

#Signup Form
class SignupForm(forms.Form):
    username = forms.CharField(
        max_length=20,
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username', 'required': 'true'})
    )
    password=forms.CharField(
        max_length=20,
        required=True,
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password', 'required': 'true'})
    )

class PastesForm(forms.ModelForm):
    class Meta:
        model=Pastes
        #fields=['title','type','expiryon','content','code','user']
        exclude=['code','user']
    title = forms.CharField(
        max_length=64,
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Title', 'required': 'true'})
    )
    type = forms.CharField(
        max_length=64,
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Type(Defalut: text)', 'required': 'true', 'value':'text'})
    )
    expiryon = forms.DateField(
        required=True,
        widget=forms.DateInput(attrs={'class': 'form-control', 'placeholder': 'YYYY-MM-DD', 'required': 'true'})
    )
    content = forms.CharField(
        max_length=500000,
        required=True,
        widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'content', 'required': 'true','cols':100,'rows':10})
    )


