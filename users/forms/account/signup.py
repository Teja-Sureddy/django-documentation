from allauth.account.forms import SignupForm
from django import forms
from phonenumber_field.formfields import PhoneNumberField
from django.utils.translation import gettext_lazy as _
from users.utils import common_as_div


class CustomSignupForm(SignupForm):
    name = forms.CharField(label=_('Name'), max_length=150, widget=forms.TextInput(attrs={"placeholder": _("Name")}))
    phone = PhoneNumberField(label=_('Phone'), widget=forms.TextInput(attrs={"placeholder": _("Phone")}))

    def save(self, request):
        user = super(CustomSignupForm, self).save(request)
        user.name = self.cleaned_data['name']
        user.phone = self.cleaned_data['phone']
        user.save()
        return user

    def as_div(self):
        return common_as_div(self)
