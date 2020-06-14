from django import forms
from django.contrib.auth import password_validation
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from seance.models import AdvUser


class RegistrationForm(forms.ModelForm):
    username = forms.CharField(required=True, widget=forms.TextInput(attrs={'placeholder': _('username')}))
    password1 = forms.CharField(required=True,
                                widget=forms.PasswordInput(attrs={'placeholder': _('password')}),
                                help_text=password_validation.password_validators_help_text_html())
    password2 = forms.CharField(required=True,
                                widget=forms.PasswordInput(attrs={'placeholder': _('repeat password')}),
                                help_text=_('Enter the same password for check please'))

    class Meta:
        model = AdvUser
        fields = ('username', 'password1', 'password2')

    def clean_password1(self):
        """
        Validates password1 to satisfy requirements for passwords
        """
        password1 = self.cleaned_data.get('password1')
        if password1:
            password_validation.validate_password(password1)
        return password1

    def clean(self):
        """
        Checks that password1 is equal with password2
        """
        super().clean()
        password1, password2 = self.cleaned_data.get('password1'), self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            errors = {'password2': ValidationError(_('passwords mismatch'), code='password_mismatch')}
            raise ValidationError(errors)

    def is_valid(self):
        return super(RegistrationForm, self).is_valid()

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user
