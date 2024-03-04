from django import forms
from .models import User, FavouritePaper


class LogInForm(forms.Form):
    username = forms.CharField(label="Username")
    password = forms.CharField(label="Password", widget=forms.PasswordInput())


class SignUpForm(forms.ModelForm):
    class Meta:
        model = User

        fields = ['username', 'email']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
        }

    newPassword = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    passwordConfirmation = forms.CharField(label='Password confirmation',
                                           widget=forms.PasswordInput(attrs={'class': 'form-control'}))


class FavouritePaperForm(forms.ModelForm):
    class Meta:
        model = FavouritePaper
        fields = ['title', 'url', 'research_question']
