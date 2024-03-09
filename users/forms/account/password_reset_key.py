from allauth.account.forms import ResetPasswordKeyForm
from users.utils import common_as_div


class CustomPasswordResetKeyForm(ResetPasswordKeyForm):
    def as_div(self):
        return common_as_div(self)
