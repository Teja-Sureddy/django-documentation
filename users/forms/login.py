from django import forms
from users.models import User
from django.core.exceptions import ValidationError


class LoginForm(forms.Form):
    email_or_phone = forms.CharField(label='Email or Phone')
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    otp = forms.CharField(label="OTP", required=False)

    def clean_email_or_phone(self):
        email_or_phone = self.cleaned_data.get("email_or_phone")
        if '@' in email_or_phone:
            try:
                User.objects.get(email=email_or_phone)
            except User.DoesNotExist:
                raise ValidationError("This email is not registered.")
        else:
            if not email_or_phone.isdigit() or len(email_or_phone) != 10:
                raise ValidationError("Invalid phone number. Please enter a 10-digit number.")
            try:
                User.objects.get(phone=email_or_phone)
            except User.DoesNotExist:
                raise ValidationError("This phone number is not registered.")
        return email_or_phone

    def clean_password(self):
        password = self.cleaned_data.get("password")
        if len(password) < 8:
            raise ValidationError("Password must be at least 8 characters long.")
        return password
