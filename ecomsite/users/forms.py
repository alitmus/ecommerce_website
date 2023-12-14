from django import forms 
from django.contrib.auth.models import  User
from django.contrib.auth.forms import  UserCreationForm,UserChangeForm
from .models import Address,Profile
class RegisterForm(UserCreationForm):
    email=forms.EmailField()


    class Meta:
        model=User
        fields=['username','email','password1','password2']


class AddressForm(forms.ModelForm) :

    class Meta:
        model= Address
        fields='__all__'
        exclude = ('user',)      

class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email','username','password',)  