from allauth.account.forms import LoginForm
from users.utils import common_as_div


class CustomLoginForm(LoginForm):
    def save(self, request):
        user = super(CustomLoginForm, self).login(request)
        return user

    def as_div(self):
        return common_as_div(self)
