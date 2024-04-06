from django.shortcuts import render, reverse
from my_apps.users.forms import ProfilePicForm, ProofForm, DescriptionForm
from django.views import View
from django.contrib import messages
from my_apps.users.models import Profile
from my_apps.users.utils import image_to_thumbnail
from my_apps.users.models.profile import get_profile_thumb_path
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

        self.send_error_message(form)
        context = self.get_context(form, form_type)
        response = render(self.request, 'profile.html', context)
        return push_url(response, request.path)

    def send_error_message(self, form):
        message = 'Error updating profile..'
        if form.errors:
            for field, errors in form.errors.as_data().items():
                if errors:
                    message = errors[0].message
                    break
        messages.error(self.request, message)

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
            profile = Profile.objects.get(user=self.request.user)
        except Profile.DoesNotExist:
            profile = None
        return profile
