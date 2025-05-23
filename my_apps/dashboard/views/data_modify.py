from django.shortcuts import redirect
from my_apps.dashboard.forms import FullDataForm
from django.contrib import messages
from django.views import View
from django.shortcuts import render, get_object_or_404
from my_apps.dashboard.models import FullData
from my_apps.users.utils import is_authorized


class DataModifyView(View):
    @is_authorized(permissions=['post_data'])
    def get(self, request, pk=None):
        context = {
            'title': self.get_text(pk, 'title'), 'pk': pk,
            'form': self.get_full_data_form(pk)
        }
        return render(request, 'data_modify.html', context)

    @is_authorized(permissions=['post_data'])
    def post(self, request, pk=None):
        if pk == 'None':
            pk = None
        form = FullDataForm(request.POST, pk=pk, context={'request': request})

        if form.is_valid():
            form.save()
            messages.success(request, self.get_text(pk, 'message'))
            return self.get_text(pk, 'path')

        if bool(self.request.GET.get('ignore_validation', False)):
            form.errors.clear()

        context = {
            'title': self.get_text(pk, 'title'),
            'pk': pk, 'form': form
        }
        return render(request, 'data_modify.html', context)

    # Utils
    def get_full_data_form(self, pk):
        instance = get_object_or_404(FullData, pk=pk) if pk else None
        if instance:
            return FullDataForm(instance=instance, initial=self.get_initials(instance), context={'request': self.request})
        return FullDataForm(context={'request': self.request})

    @staticmethod
    def get_initials(instance):
        return {
            'name': instance.data.name,
            'email': instance.data.email,
            'age': instance.data.age,
            'gender': instance.data.gender,
            'dob': instance.data.dob,
            'tob': instance.data.tob,
            'slug': instance.data.slug,
            'website': instance.data.website,
            'ip_address': instance.data.ip_address
        }

    @staticmethod
    def get_text(pk, text_type):
        if text_type == 'title':
            return f'{"Edit" if pk else "Add" } Data'
        elif text_type == 'message':
            return f'{"Updated" if pk else "Added"}.'
        elif text_type == 'path':
            return redirect('dashboard:data-edit', pk=pk) if pk else redirect('dashboard:data-add')
