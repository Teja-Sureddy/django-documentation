from django.forms import ModelForm, Textarea
from users.models import ProfileModel
from django.core.exceptions import ValidationError
from users.utils import common_as_div


class ProfilePicForm(ModelForm):
    class Meta:
        model = ProfileModel
        fields = ['profile_pic']

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

    def as_div(self):
        profile_src = self.instance.profile_pic.url if self.instance else '/assets/public/default_pic.jpg'
        html = ''
        for field in self:
            html += f'''
                <div class="w-h-150 mx-auto">
                    <label for="{field.id_for_label}">
                        <img src="{profile_src}" width="150px" alt="Profile Picture" class="rounded-circle p-1 profile-pic">
                    </label>
                    <div class="d-none">{field.as_widget()}</div>
                </div>
            '''
        return html


class ProofForm(ModelForm):
    class Meta:
        model = ProfileModel
        fields = ['proof']

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

    def as_div(self):
        proof_href = self.instance.proof.url if self.instance else None
        html = ''
        for field in self:
            html += f'''
                <div class="d-flex flex-row align-items-center fs-9">
                    <div class="me-2">
                        {f'<a href="{proof_href}" target="_blank">Preview</a>' if proof_href else 'No Proof Found'}
                    </div>
                    <div>
                        <label for="{field.id_for_label}">
                            <a class="btn btn-primary fs-9 p-2 text-white"><i class="bi bi-cloud-arrow-up-fill"></i></a>
                        </label>
                        <div class="d-none">{field.as_widget()}</div>
                    </div>
                </div>
            '''
        return html


class DescriptionForm(ModelForm):
    class Meta:
        model = ProfileModel
        fields = ['description']
        labels = {'description': 'Description'}
        widgets = {'description': Textarea(attrs={'class': 'h-150', 'placeholder': 'Enter your description here'})}

    def as_div(self):
        return common_as_div(self)
