from registration.forms import RegistrationForm
from django.contrib.auth.forms import AuthenticationForm
from django.forms import ModelForm

from django import forms
from django.utils.translation import ugettext_lazy as _


class UserRegForm(RegistrationForm):
    first_name = forms.CharField(label=_('First name'), required=False)
    last_name = forms.CharField(label=_('Last name'), required=False)

    job_description = forms.CharField(label=_('Function'), required=False)
    organisation = forms.CharField(label=_('Organisation'), required=False)

    country = forms.CharField(label=_('Country'), required=False)

    newsletter = forms.BooleanField(label=_('Send me the newsletter'), initial=False)
    updates_tool_developments = forms.BooleanField(label=_('Send updates on tool developments'), initial=False)
    next = forms.CharField(_('next'), required=False, widget=forms.HiddenInput())


class LoginForm(AuthenticationForm):
    next = forms.CharField(_('next'), required=False, widget=forms.HiddenInput())