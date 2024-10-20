from django import forms
from .models import SafetyAlert, Profile


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
