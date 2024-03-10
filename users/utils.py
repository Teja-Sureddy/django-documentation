from django import forms
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from allauth.account.utils import user_field
from django.core.exceptions import PermissionDenied
from django.contrib.auth.models import Permission
from PIL import Image
import os
from my_project.settings import MEDIA_URL


def common_as_div(self):
    html = ''
    for field in self:
        if isinstance(field.field, forms.BooleanField):
            html += f"""
                <div class='mb-3 d-flex flex-row justify-content-start'>
                    <div class='data-form'>{field.as_widget()}</div>
                    <label class='form-label mb-2 ms-2 fs-9' for="{field.id_for_label}">
                    {field.label}
                    <span class='text-danger'>{'*' if field.field.required and field.label else ''}</span>
                    </label>
                    <div class='text-danger fs-9 mt-1'>{field.errors}</div>
                </div>
            """
        else:
            html += f"""
                <div class='mb-3 d-flex flex-column justify-content-start'>
                    <label class='form-label mb-2 fs-9' for="{field.id_for_label}">
                    {field.label}
                    <span class='text-danger'>{'*' if field.field.required and field.label else ''}</span>
                    </label>
                    <div class='data-form'>{field.as_widget()}</div>
                    <div class='text-danger fs-9 mt-1'>{field.errors}</div>
                </div>
            """

    errors = '<div class="mb-3 fs-9">'
    for field, error in self.errors.items():
        errors += f'{error}' if field == '__all__' else ''
    errors += '</div>'

    html += errors if self.errors else ''
    return html


# Custom Social Adapter to save the name while sign up
class CustomSocialAccountAdapter(DefaultSocialAccountAdapter):
    def populate_user(self, request, sociallogin, data):
        user = super().populate_user(request, sociallogin, data)
        first_name = data.get("first_name")
        last_name = data.get("last_name")
        user_field(user, "name", f"{first_name} {last_name}")
        return user


def is_authorized(groups=[], permissions=[]):
    def decorator(view_func):
        def wrapper(*args, **kwargs):
            request = args[0].request if hasattr(args[0], 'request') else args[0]
            user = getattr(request, 'user', None)

            user_group_permissions = Permission.objects.filter(group__user=user)
            group_filter = any(query_set.codename in groups for query_set in user_group_permissions)

            user_permissions = Permission.objects.filter(user=user)
            permission_filter = any(query_set.codename in permissions for query_set in user_permissions)

            if group_filter or permission_filter:
                return view_func(*args, **kwargs)

            raise PermissionDenied

        return wrapper

    return decorator


def image_to_thumbnail(form, field_name, file_path):
    thumbnail_size = (100, 100)
    image = Image.open(form.files[field_name])
    image.thumbnail(thumbnail_size)

    full_file_path = os.path.join(MEDIA_URL, file_path)
    directory = os.path.dirname(full_file_path)
    os.makedirs(directory, exist_ok=True)
    image.save(full_file_path)
