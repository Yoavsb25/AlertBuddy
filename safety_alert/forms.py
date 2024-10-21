from django import forms
from .models import SafetyAlert, Profile
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email']

class SafetyAlertForm(forms.ModelForm):
    class Meta:
        model = SafetyAlert
        fields = ['user_location', 'status']
        widgets = {
            'status': forms.RadioSelect(choices=[(True, 'Safe'), (False, 'Not Safe')]),
            'user_location': forms.TextInput(attrs={'class': 'form-control'}),
        }


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
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        if commit:
            user.save()
        return user