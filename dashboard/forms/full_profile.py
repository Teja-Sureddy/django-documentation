from django import forms
from dashboard.models import ProfileModel, FullProfileModel


class FullProfileForm(forms.ModelForm):
    class Meta:
        model = FullProfileModel
        fields = ['name', 'email', 'age', 'gender', 'dob', 'tob', 'slug', 'website', 'ip_address',
                  'hair', 'hair_color', 'color', 'duration', 'json_data']

    name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'placeholder': 'Enter your Name'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'placeholder': 'Enter your Email'}))
    age = forms.IntegerField(widget=forms.NumberInput(attrs={'placeholder': 'Enter your Age'}))
    gender = forms.ChoiceField(choices=[('', 'Select gender'), ] + ProfileModel.GENDERS)
    dob = forms.DateField(label='Date of birth', widget=forms.DateInput(attrs={'placeholder': 'YYYY-MM-DD'}))
    tob = forms.TimeField(label='Time of birth', widget=forms.TimeInput(attrs={'placeholder': 'HH:MM'}))
    slug = forms.SlugField(widget=forms.TextInput(attrs={'placeholder': 'Enter slug'}))
    website = forms.URLField(initial='https://', widget=forms.URLInput(attrs={'placeholder': 'Enter website URL'}))
    ip_address = forms.GenericIPAddressField(widget=forms.TextInput(attrs={'placeholder': 'Enter IP address'}))

    def save(self, commit=True):
        profile_data = {
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
        profile = ProfileModel.objects.create(**profile_data)
        self.cleaned_data['profile'] = profile
        self.instance.profile = profile
        full_profile = super().save(commit=commit)
        full_profile.color.set(self.cleaned_data['color'])
        return full_profile

    def as_div(self):
        html = ''
        for field in self:
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
        return html

    def __init__(self, *args, **kwargs):
        super(FullProfileForm, self).__init__(*args, **kwargs)
        self.fields['hair'].empty_label = 'Select hair'
        self.fields['hair_color'].choices = [('', 'Select hair color')] + FullProfileModel.HairColor.choices
        self.fields['duration'].widget.attrs['placeholder'] = 'Enter duration'
        self.fields['json_data'].widget.attrs['placeholder'] = 'Enter JSON'
