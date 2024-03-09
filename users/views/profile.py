from django.shortcuts import render, redirect
from users.forms import ProfileForm
from django.views import View
from django.contrib import messages
from users.models import ProfileModel
from users.utils import image_to_thumbnail
from users.models.profile import get_profile_thumb_path


class ProfileView(View):
    def get(self, request):
        context = {
            'title': 'Profile', 'form': ProfileForm()
        }
        return render(request, 'profile.html', context)

    def post(self, request):
        profile = self.get_profile()
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.user = request.user

            # Profile thumbnail
            thumb_path = get_profile_thumb_path(request, form.files['profile_pic'].name)
            image_to_thumbnail(form, 'profile_pic', thumb_path)
            profile.profile_thumb = thumb_path

            profile.save()
            messages.success(request, 'Profile updated.')
            return redirect('users:profile')

        context = {
            'title': 'Profile', 'form': form
        }
        return render(request, 'profile.html', context)

    def get_profile(self):
        try:
            profile = ProfileModel.objects.get(user=self.request.user)
        except ProfileModel.DoesNotExist:
            profile = None
        return profile
