from django.shortcuts import render, reverse
from users.forms import ProfilePicForm, ProofForm, DescriptionForm
from django.views import View
from django.contrib import messages
from users.models import ProfileModel
from users.utils import image_to_thumbnail
from users.models.profile import get_profile_thumb_path
from django_htmx.http import HttpResponseClientRedirect, push_url


class ProfileView(View):
    def get(self, request):
        context = self.get_context()
        return render(request, 'profile.html', context)

    def post(self, request):
        profile_instance = self.get_profile()
        form_type = request.GET.get('type')
        form = None
        if form_type == 'profile_pic':
            form = ProfilePicForm(request.POST, request.FILES, instance=profile_instance)
        elif form_type == 'description':
            form = DescriptionForm(request.POST, request.FILES, instance=profile_instance)
        elif form_type == 'proof':
            form = ProofForm(request.POST, request.FILES, instance=profile_instance)

        if form.is_valid():
            profile = form.save(commit=False)
            profile.user = request.user

            if form_type == 'profile_pic':
                # Profile thumbnail
                thumb_path = get_profile_thumb_path(request, form.files['profile_pic'].name)
                image_to_thumbnail(form, 'profile_pic', thumb_path)
                profile.profile_thumb = thumb_path

            profile.save()
            messages.success(request, 'Profile updated.')
            return HttpResponseClientRedirect(reverse('users:profile'))

        context = self.get_context(form, form_type)
        messages.error(request, 'Error updating profile..')
        response = render(self.request, 'profile.html', context)
        return push_url(response, request.path)

    def get_context(self, form=None, form_type=None):
        profile = self.get_profile()
        context = {
            'title': 'Profile',
            'user': self.request.user,
            'profile': profile,
            'profile_form': form if form_type == 'profile_pic' else ProfilePicForm(instance=profile),
            'description_form': form if form_type == 'description' else DescriptionForm(instance=profile),
            'proof_form': form if form_type == 'proof' else ProofForm(instance=profile)
        }
        return context

    def get_profile(self):
        try:
            profile = ProfileModel.objects.get(user=self.request.user)
        except ProfileModel.DoesNotExist:
            profile = None
        return profile
