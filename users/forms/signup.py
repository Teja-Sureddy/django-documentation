from django import forms
from users.models import User


class SignupForm():
    phone = forms.IntegerField(required=True)

    def custom_signup(self, request, user):
        # Save extra fields to the user object
        user.phone = self.cleaned_data['phone']
        user.save()

    def save(self, request):
        user = super(SignupForm, self).save(request)
        self.custom_signup(request, user)
        return user

    # def __init__(self, *args, **kwargs):
    #     super(SignupForm, self).__init__(*args, **kwargs)
    #     self.fields["phone"] = forms.IntegerField(label='Phone Number')
    #
    # def clean(self):
    #     super(SignupForm, self).clean()
    #
    # def save(self, request):
    #     email = self.cleaned_data.get("email")
    #     if self.account_already_exists:
    #         raise ValueError(email)
    #     adapter = get_adapter()
    #     user = adapter.new_user(request)
    #     adapter.save_user(request, user, self, False)
    #     setattr(user, "phone", self.cleaned_data.get("phone"))
    #     print(1)
    #
    # def custom_signup(self, request, user):
    #     user.name = self.cleaned_data['name']
    #     user.email = self.cleaned_data['last_name']
    #     user.phone = self.cleaned_data['phone']
    #     user.save()
