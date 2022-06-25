from django import forms
from django.core.validators import RegexValidator
from django.contrib.auth.models import User
import re 
from .models import Profile, Setting

class LoginForm(forms.Form):
    username = forms.CharField(validators=[RegexValidator(
                regex='^[a-zA-Z]+$',
                message='Name must be letters only!',
                code='errors'
            )])
    password = forms.CharField(widget=forms.PasswordInput)

def username_validator(texty):
    if re.match(r'^[a-zA-Z]+$', texty):
        return texty
    else:
        raise forms.ValidationError('Name must be letters only!')

class UserRegistrationForm(forms.ModelForm):
    username = forms.CharField(
        label='Name:',
        widget=forms.TextInput(attrs={'autofocus': True}),
        validators=[username_validator])
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2= forms.CharField(label='Confirm Password', widget=forms.PasswordInput)

    class Meta:
        model =  User
        fields = ('username', 'email')

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Passwords do not match.')
        return cd

class ProfileEditForm(forms.ModelForm):
    bio = forms.CharField(max_length=228, widget=forms.Textarea(attrs={'rows':4}))
    class Meta:
        model = Profile
        fields = ('display_name', 'text_color','accent_color', 'bg','image', 'photo', 'bio', 'website', 'phone')
        widgets = {
            'text_color': forms.TextInput(attrs={'type': 'color'}),
            'accent_color': forms.TextInput(attrs={'type': 'color'}),
        }


class SettingForm(forms.ModelForm):
    class Meta:
        model = Setting
        fields = ('ciphers',)
        widgets = {'ciphers' : forms.CheckboxSelectMultiple()}