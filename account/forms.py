from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import PortUser
from django.contrib.auth.forms import AuthenticationForm
from django import forms


class PortUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm):
        model = PortUser
        fields = ('full_name','email','billing_address')

class PortUserChangeForm(UserChangeForm):
    class Meta:
        model = PortUser
        fields = ('email',)


class UserLoginForm(AuthenticationForm):
    class Meta:
        model = PortUser

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class': "my_class",'placeholder':'Your email address'})
        self.fields['password'].widget.attrs.update({'class': "my_class",'placeholder':'Password'})

class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = PortUser
        fields = ('email','full_name','billing_address')

