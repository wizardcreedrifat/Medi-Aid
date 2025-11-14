from logging import PlaceHolder
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, SetPasswordForm, PasswordChangeForm, PasswordResetForm, UsernameField
from django.utils.translation import gettext, gettext_lazy as _
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.contrib.auth import password_validation
from .models import Doctor, Patient, InsuranceProvider, Prescription

class RegistrationForm(UserCreationForm):
        email = forms.CharField(label="Email", required=True, widget=forms.EmailInput(attrs={'class':'form-control','placeholder':'Email', 'style':'opacity:0.8'}))
        username = forms.CharField(label="Username", widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Username', 'style':'opacity:0.8'}))
        password1 = forms.CharField(label="Password", widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'Password', 'style':'opacity:0.8'}))
        password2 = forms.CharField(label="Confirm Password", widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'Confirm Password', 'style':'opacity:0.8'}))
        class Meta:
            model = User
            fields = ['username', 'email', 'password1', 'password2']

class LoginForm(AuthenticationForm):
    username = UsernameField(widget=forms.TextInput(attrs={'class':'form-control', 'PlaceHolder':'Username', 'style':'opacity:0.8; color:black'}))
    password = forms.CharField(label=_("Password"), strip=False, widget=forms.PasswordInput(attrs={'autocomplete':'current-password',
    'class':'form-control', 'PlaceHolder':'Password', 'style':'opacity:0.8;'}))


class MyPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(label=_("Old Password"), strip=False, widget=forms.PasswordInput(attrs={'autocomplete':'current-password',
    'autofocus':True,'class':'form-control'}))
    new_password1 = forms.CharField(label=_("New Password"), strip=False, widget=forms.PasswordInput(attrs={'autocomplete':'new-password',
    'class':'form-control'}),help_text = password_validation.password_validators_help_text_html())
    new_password2 = forms.CharField(label=_("Confirm New Password"), strip=False, widget=forms.PasswordInput(attrs={'autocomplete':'new-password',
    'class':'form-control'}))

class MyPasswordResetForm(PasswordResetForm):
    email = forms.EmailField(label=_("Email"), max_length=254, widget=forms.EmailInput(attrs={'autocomplete':'email',
    'class':'form-control'}))

class MySetPasswordForm(SetPasswordForm):
    new_password1 = forms.CharField(label=_("New Password"), strip=False, widget=forms.PasswordInput(attrs={'autocomplete':'new-password',
    'class':'form-control'}),help_text = password_validation.password_validators_help_text_html())
    new_password2 = forms.CharField(label=_("Confirm New Password"), strip=False, widget=forms.PasswordInput(attrs={'autocomplete':'new-password',
    'class':'form-control'}))


class InsuranceRegForm(forms.ModelForm):
    class Meta:
        model = InsuranceProvider
        fields = ['name' ,'number' ,'address', 'policy']
        widgets = {
                    'name':forms.TextInput(attrs={'class':'form-control', 'placeholder':'Company Name'}),
                    'number':forms.TextInput(attrs={'class':'form-control', 'placeholder':'Phone Number'}),
                    'address':forms.TextInput(attrs={'class':'form-control', 'placeholder':'Address'}),
                    'policy':forms.Textarea(attrs={'class':'form-control', 'placeholder':'Policy Description'})
                    }
        

class DoctorUpdateForm(forms.ModelForm):
    class Meta:
        model = Doctor
        fields = ['name' ,'number' ,'hospital', 'speciality', 'qualification', 'availability', 'start', 'end', 'fees', 'profilepic']
        widgets = {
                    'name':forms.TextInput(attrs={'class':'form-control', 'placeholder':'Name'}),
                    'number':forms.TextInput(attrs={'class':'form-control', 'placeholder':'Number'}),
                    'hospital':forms.TextInput(attrs={'class':'form-control', 'placeholder':'Hospital'}),
                    'speciality':forms.Textarea(attrs={'class':'form-control', 'placeholder':'Speciality'}),
                    'qualification':forms.Textarea(attrs={'class':'form-control', 'placeholder':'Qualification'}),
                    'availability':forms.TextInput(attrs={'class':'form-control', 'placeholder':'Availability'}),
                    'start':forms.TextInput(attrs={'class':'form-control', 'placeholder':'Start'}),
                    'end':forms.TextInput(attrs={'class':'form-control', 'placeholder':'End'}),
                    'fees':forms.TextInput(attrs={'class':'form-control', 'placeholder':'Fees'}),
                    'profilepic':forms.FileInput(attrs={'class':'form-control'}),
                    }
        

class PatientUpdateForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = ['name' ,'number' ,'medications', 'disease', 'allergy', 'insurance', 'profilepic']
        widgets = {
                    'name':forms.TextInput(attrs={'class':'form-control', 'placeholder':'Name'}),
                    'number':forms.TextInput(attrs={'class':'form-control', 'placeholder':'Number'}),
                    'insurance':forms.TextInput(attrs={'class':'form-control', 'placeholder':'Insurance company id'}),
                    'medications':forms.Textarea(attrs={'class':'form-control', 'placeholder':'medications'}),
                    'disease':forms.Textarea(attrs={'class':'form-control', 'placeholder':'Disease'}),
                    'allergy':forms.Textarea(attrs={'class':'form-control', 'placeholder':'Allergy'}),
                    'profilepic':forms.FileInput(attrs={'class':'form-control'}),
                    }


class DoctorForm(forms.ModelForm):
    class Meta:
        model = Doctor
        fields = ['profilepic']
        widgets = {
                'profilepic':forms.FileInput(attrs={'class':'form-control'}),
        }
