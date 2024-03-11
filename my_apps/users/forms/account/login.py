from allauth.account.forms import LoginForm
from my_apps.users.utils import common_as_div


class CustomLoginForm(LoginForm):
    def as_div(self):
        return common_as_div(self)
