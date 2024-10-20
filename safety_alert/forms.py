from django import forms
from .models import SafetyAlert, Profile
from django.contrib.auth.models import User

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
