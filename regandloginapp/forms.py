from django import forms
from .models import Reg
class RegForm(forms.ModelForm):
    class Meta:
        model = Reg
        widgets = {'password': forms.PasswordInput(),'cpassword': forms.PasswordInput(), }
        fields = ['username', 'password','cpassword','fname','lname','dob','mobno','emailid']
class LoginForm(forms.Form):
    username = forms.CharField(max_length=20)
    password = forms.CharField(widget=forms.PasswordInput())



