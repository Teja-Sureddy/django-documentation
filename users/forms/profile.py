from django.forms import ModelForm
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
                <div class="form-group">
                    <label for="{field.id_for_label}">
                        <img src="{profile_src}" width="100px" alt="Profile Picture">
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
                <div class="form-group">
                    { f'<a href="{proof_href}" target="_blank">Proof</a>' if proof_href else '' }
                    <label for="{field.id_for_label}">Upload</label>
                    <div class="d-none">{field.as_widget()}</div>
                </div>
            '''
        return html


class DescriptionForm(ModelForm):
    class Meta:
        model = ProfileModel
        fields = ['description']

    def as_div(self):
        return common_as_div(self)
