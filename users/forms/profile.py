from django import forms
from users.models import ProfileModel
from users.utils import common_as_div
from django.core.exceptions import ValidationError


class ProfileForm(forms.ModelForm):
    class Meta:
        model = ProfileModel
        fields = ['proof', 'profile_pic', 'description']

    def as_div(self):
        return common_as_div(self)

    def clean_profile_pic(self):
        profile_pic = self.cleaned_data.get('profile_pic')
        size = 1 * 1024 * 1024
        allowed_extensions = ('.png', '.jpg')
        if profile_pic:
            if profile_pic.size > size:
                raise ValidationError(f"Profile picture file size must be less than {int(size / (1024 * 1024))}MB.")
            if not profile_pic.name.lower().endswith(allowed_extensions):
                raise ValidationError(f"Profile picture must be in {', '.join(allowed_extensions)} format.")
        return profile_pic

    def clean_proof(self):
        proof = self.cleaned_data.get('proof')
        size = 2 * 1024 * 1024
        allowed_extensions = ('.pdf',)
        if proof:
            if proof.size > size:
                raise ValidationError(f"Proof file size must be less than {int(size / (1024 * 1024))}MB.")
            if not proof.name.lower().endswith(allowed_extensions):
                raise ValidationError(f"Proof must be in {', '.join(allowed_extensions)} format.")
        return proof
