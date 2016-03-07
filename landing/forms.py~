from cabinet_webmaster.models import CabinetWebmasterModel
from django.contrib.auth.models import User
from django import forms

#username,email,password,first_name,last_name
class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    first_name = forms.CharField(required=False)
    last_name = forms.CharField(required=False)
    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'first_name', 'last_name')

class CabinetWebmasterForm(forms.ModelForm):
    wmr = forms.CharField(required=False)
    mobile_phone = forms.CharField(required=False)
    skype = forms.CharField(required=False)
    class Meta:
        model = CabinetWebmasterModel
        fields = ('wmr', 'mobile_phone', 'skype')
