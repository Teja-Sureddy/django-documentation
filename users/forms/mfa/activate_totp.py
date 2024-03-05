from allauth.mfa.forms import ActivateTOTPForm
from users.utils import common_as_div


class CustomActivateTOTPForm(ActivateTOTPForm):
    def as_div(self):
        return common_as_div(self)
