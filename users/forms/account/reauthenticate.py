from allauth.account.forms import ReauthenticateForm
from users.utils import common_as_div


class CustomReauthenticateForm(ReauthenticateForm):
    def as_div(self):
        return common_as_div(self)
