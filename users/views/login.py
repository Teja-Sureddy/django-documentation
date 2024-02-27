from django.shortcuts import render, reverse
from users.forms import LoginForm
from django_htmx.http import push_url, HttpResponseClientRedirect
from django.views import View


class LoginView(View):
    def get(self, request):
        form = LoginForm()
        del form.fields['otp']

        context = {
            'title': 'Login',
            'form': form
        }
        return render(request, 'login.html', context)

    def post(self, request):
        form = LoginForm(request.POST)
        if 'otp' not in form.changed_data:
            del form.fields['otp']
        if form.is_valid():
            email_or_phone = form.cleaned_data.get("email_or_phone")
            password = form.cleaned_data.get("password")
            otp = form.cleaned_data.get("otp")
            print(email_or_phone, password, otp)

            if not otp:
                response = render(request, 'login.html', {'form': form})
                return push_url(response, request.path)
            else:
                response = reverse('profile')
                return HttpResponseClientRedirect(response)

        response = render(request, 'login.html', {'form': form})
        url = push_url(response, request.path)
        return url
