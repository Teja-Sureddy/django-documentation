from django.shortcuts import redirect
from dashboard.forms import FullProfileForm
from django.contrib import messages
from django.views import View
from django.shortcuts import render, get_object_or_404
from dashboard.models import FullProfileModel


class ProfileModifyView(View):
    def get(self, request, pk=None):
        context = {
            'title': self.get_text(pk, 'title'), 'pk': pk,
            'form': self.get_full_profile_form(pk)
        }
        return render(request, 'profile_modify.html', context)

    def post(self, request, pk=None):
        if pk == 'None':
            pk = None
        form = FullProfileForm(request.POST, pk=pk)

        if form.is_valid():
            form.save()
            messages.success(request, self.get_text(pk, 'message'))
            return self.get_text(pk, 'path')

        context = {
            'title': self.get_text(pk, 'title'),
            'pk': pk, 'form': form
        }
        return render(request, 'profile_modify.html', context)

    # Utils
    def get_full_profile_form(self, pk):
        instance = get_object_or_404(FullProfileModel, pk=pk) if pk else None
        if instance:
            return FullProfileForm(instance=instance, initial=self.get_initials(instance))
        return FullProfileForm()

    @staticmethod
    def get_initials(instance):
        return {
            'name': instance.profile.name,
            'email': instance.profile.email,
            'age': instance.profile.age,
            'gender': instance.profile.gender,
            'dob': instance.profile.dob,
            'tob': instance.profile.tob,
            'slug': instance.profile.slug,
            'website': instance.profile.website,
            'ip_address': instance.profile.ip_address
        }

    @staticmethod
    def get_text(pk, text_type):
        if text_type == 'title':
            return f'{"Edit" if pk else "Add" } Profile'
        elif text_type == 'message':
            return f'{"Updated" if pk else "Added"}.'
        elif text_type == 'path':
            return redirect('dashboard:profile-edit', pk=pk) if pk else redirect('dashboard:profile-add')
