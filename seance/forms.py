from django import forms
from django.contrib.auth import password_validation
from django.utils.translation import gettext_lazy as _

from seance.models import AdvUser


class RegistrationForm(forms.ModelForm):
    password1 = forms.CharField(required=True, widget=forms.PasswordInput,
                                help_text=password_validation.password_validators_help_text_html())
    password2 = forms.CharField(required=True, widget=forms.PasswordInput,
                                help_text=_('Enter the same password for check please'))

    class Meta:
        model = AdvUser
        fields = ('username', 'password1', 'password2')
