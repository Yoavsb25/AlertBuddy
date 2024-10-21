from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import SafetyAlert, Profile
from django.core.exceptions import ValidationError


class UserProfileEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name']

    def save(self, commit=True):
        user = super(UserProfileEditForm, self).save(commit=False)
        user.first_name = user.first_name.lower().capitalize()
        user.last_name = user.last_name.lower().capitalize()

        if commit:
            user.save()
        return user


class SafetyAlertForm(forms.ModelForm):
    class Meta:
        model = SafetyAlert
        fields = ['user_location', 'status']
        widgets = {
            'status': forms.RadioSelect(choices=[(True, 'Safe'), (False, 'Not Safe')]),
            'user_location': forms.TextInput(attrs={'class': 'form-control'}),
        }

class EmailAuthenticationForm(AuthenticationForm):
    username = forms.EmailField(label='Email', max_length=254)

class UserSearchForm(forms.Form):
    username = forms.CharField(label='Search for a friend', max_length=150)

class ProfileImageForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['profile_image']

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'password1', 'password2']

    def save(self, commit=True):
        user = super(CustomUserCreationForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        user.username = self.cleaned_data['email']  # Set username to email
        # Capitalize first and last name
        user.first_name = self.cleaned_data['first_name'].capitalize()
        user.last_name = self.cleaned_data['last_name'].capitalize()

        if commit:
            user.save()
        return user