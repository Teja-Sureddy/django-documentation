from allauth.mfa.forms import AuthenticateForm
from users.utils import common_as_div


class CustomAuthenticateForm(AuthenticateForm):
    def as_div(self):
        return common_as_div(self)
