from django import forms
from .models import User, FavouritePaper


class LogInForm(forms.Form):
    username = forms.CharField(label="Username")
    password = forms.CharField(label="Password", widget=forms.PasswordInput())


class SignUpForm(forms.ModelForm):
    newPassword = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    passwordConfirmation = forms.CharField(label='Password confirmation', widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ['username', 'email']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('newPassword')
        confirm_password = cleaned_data.get('passwordConfirmation')

        if password and confirm_password and password != confirm_password:
            self.add_error('passwordConfirmation', 'Password confirmation does not match Password')

        return cleaned_data


class FavouritePaperForm(forms.ModelForm):
    class Meta:
        model = FavouritePaper
        fields = ['article']

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(FavouritePaperForm, self).__init__(*args, **kwargs)

    def save(self, commit=True):
        instance = super(FavouritePaperForm, self).save(commit=False)
        if self.user:
            instance.user = self.user
        if commit:
            instance.save()
        return instance


class SearchForm(forms.Form):
    query = forms.CharField(
        label="Search Query",
        max_length=500,
        error_messages={
            'max_length': "Your search query exceeds the maximum allowed length of characters."
        }
    )