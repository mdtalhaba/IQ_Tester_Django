from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import Review


class RegistrationForm(UserCreationForm):
    first_name = forms.CharField(widget=forms.TextInput(attrs={'id' : 'required'}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={'id' : 'required'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'id' : 'required'}))

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_active = False
        user.save()
        return user
    
class UserUpdateForm(UserChangeForm):
    password = None
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']


class ReviewForm(forms.ModelForm):
    class Meta:
        model : Review
        fields : ['body']