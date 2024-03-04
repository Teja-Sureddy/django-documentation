from django import forms


def common_as_div(self):
    html = ''
    for field in self:
        if isinstance(field.field, forms.BooleanField):
            html += f"""
                <div class='mb-3 d-flex flex-row justify-content-start'>
                    <div class='profile-form'>{field.as_widget()}</div>
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
                    <div class='profile-form'>{field.as_widget()}</div>
                    <div class='text-danger fs-9 mt-1'>{field.errors}</div>
                </div>
            """

    errors = '<div class="mb-3 fs-9">'
    for field, error in self.errors.items():
        errors += f'{error}' if field == '__all__' else ''
    errors += '</div>'

    html += errors
    return html
