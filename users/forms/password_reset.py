from allauth.account.forms import ResetPasswordForm
from users.utils import common_as_div


class CustomPasswordResetForm(ResetPasswordForm):
    def save(self, request, **kwargs):
        user = super(CustomPasswordResetForm, self).save(request, **kwargs)
        return user

    def as_div(self):
        return common_as_div(self)
