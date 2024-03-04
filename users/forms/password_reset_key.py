from allauth.account.forms import ResetPasswordKeyForm
from users.utils import common_as_div


class CustomPasswordResetKeyForm(ResetPasswordKeyForm):
    def save(self):
        user = super(CustomPasswordResetKeyForm, self).save()
        return user

    def as_div(self):
        return common_as_div(self)
