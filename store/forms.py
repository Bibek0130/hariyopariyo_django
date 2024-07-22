from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User

class SignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=200, help_text="Required")
    class Meta:
        model = User
        fields = ('username','email','password','password2')

class CustomAuthenticationForm(AuthenticationForm):
    username = forms.CharField(widget = forms.TextInput(attrs={'class':'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control'}))
    
CustomUserCreationForm = SignUpForm