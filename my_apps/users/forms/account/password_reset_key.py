from allauth.account.forms import ResetPasswordKeyForm
from my_apps.users.utils import common_as_div


class CustomPasswordResetKeyForm(ResetPasswordKeyForm):
    def as_div(self):
        return common_as_div(self)
