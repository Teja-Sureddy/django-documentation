from django.shortcuts import redirect
from dashboard.forms import FullProfileForm
from django.contrib import messages
from django.views import View
from django.shortcuts import render


class ProfileAddView(View):
    def get(self, request, *args, **kwargs):
        context = {
            'title': 'Add Profile',
            'form': FullProfileForm()
        }
        return render(request, 'profile_add.html', context)

    def post(self, request):
        form = FullProfileForm(request.POST)

        if form.is_valid():
            form.save()
            messages.success(request, "Added.")
            return redirect(request.path)

        context = {
            'title': 'Add Profile',
            'form': form
        }
        return render(request, 'profile_add.html', context)
