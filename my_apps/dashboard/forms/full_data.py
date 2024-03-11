from django import forms
from my_apps.dashboard.models import DataModel, FullDataModel
from dynamic_forms import DynamicFormMixin, DynamicField
from my_apps.dashboard.utils import set_dropdown_attrs

HX_ATTRIBUTES = {
    "hx-trigger": "change delay:1000ms",
    "hx-target": "#body",
}


class FullDataForm(DynamicFormMixin, forms.ModelForm):
    class Meta:
        model = FullDataModel
        fields = ['name', 'email', 'age', 'gender', 'dob', 'tob', 'slug', 'website', 'ip_address',
                  'hair', 'hair_color', 'color', 'duration', 'json_data']

    name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'placeholder': 'Enter your Name'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'placeholder': 'Enter your Email'}))
    age = forms.IntegerField(widget=forms.NumberInput(attrs={'placeholder': 'Enter your Age'}))
    gender = forms.ChoiceField(choices=[('', 'Select gender'), ] + DataModel.GENDERS)

    dob = DynamicField(
        forms.DateField,
        include=lambda form: str(form['gender'].value()) in ('M', 'F'),
        label='Date of birth',
        widget=forms.DateInput(attrs={'placeholder': 'YYYY-MM-DD'})
    )
    tob = DynamicField(
        forms.TimeField,
        include=lambda form: str(form['gender'].value()) in ('M', 'F'),
        label='Time of birth',
        widget=forms.TimeInput(attrs={'placeholder': 'HH:MM'})
    )

    slug = forms.SlugField(widget=forms.TextInput(attrs={'placeholder': 'Enter slug'}))
    website = forms.URLField(initial='https://', widget=forms.URLInput(attrs={'placeholder': 'Enter website URL'}))
    ip_address = forms.GenericIPAddressField(widget=forms.TextInput(attrs={'placeholder': 'Enter IP address'}))

    def __init__(self, *args, pk=None, **kwargs):
        self.pk = pk
        super(FullDataForm, self).__init__(*args, **kwargs)
        self.fields['hair_color'].choices = [('', 'Select hair color')] + FullDataModel.HairColor.choices
        self.fields['duration'].widget.attrs['placeholder'] = 'Enter duration'
        self.fields['json_data'].widget.attrs['placeholder'] = 'Enter JSON'

        set_dropdown_attrs(self.fields)

        path = kwargs.get('context', {}).get('request').path
        if path:
            self.fields['gender'].widget.attrs.update({"hx-post": f"{path}?ignore_validation=true", **HX_ATTRIBUTES})

    def save(self, commit=True):
        data_data = {
            'name': self.cleaned_data['name'],
            'email': self.cleaned_data['email'],
            'age': self.cleaned_data['age'],
            'dob': self.cleaned_data['dob'],
            'tob': self.cleaned_data['tob'],
            'gender': self.cleaned_data['gender'],
            'ip_address': self.cleaned_data['ip_address'],
            'slug': self.cleaned_data['slug'],
            'website': self.cleaned_data['website'],
        }

        if self.pk is not None:
            full_data = FullDataModel.objects.get(pk=self.pk)
            data = full_data.data
            data.__dict__.update(**data_data)
            data.save()
        else:
            data = DataModel.objects.create(**data_data)

        self.instance.pk = self.pk
        self.instance.data = data
        full_data = super().save(commit=commit)
        full_data.color.set(self.cleaned_data['color'])
        return full_data

    def as_div(self):
        html = ''
        for field in self:
            html += f"""
                <div class='mb-3 px-2 d-flex flex-column justify-content-start col-12 col-sm-6 col-lg-4'>
                    <label class='form-label mb-2 fs-9' for="{field.id_for_label}">
                    {field.label}
                    <span class='text-danger'>{'*' if field.field.required and field.label else ''}</span>
                    </label>
                    <div class='data-form'>{field.as_widget()}</div>
                    <div class='text-danger fs-9 mt-1'>{field.errors}</div>
                </div>
            """
        return html
