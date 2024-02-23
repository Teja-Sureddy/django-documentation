from django import forms
from dashboard.models import ProfileModel, FullProfileModel


class FullProfileForm(forms.ModelForm):
    class Meta:
        model = FullProfileModel
        fields = ['hair_color', 'duration', 'json_data', 'color', 'hair']

    name = forms.CharField(max_length=100, initial='Person')
    email = forms.EmailField(initial='Persontest@gmail.com')
    age = forms.IntegerField(initial=22)
    dob = forms.DateField(initial='2024-12-12')
    tob = forms.TimeField(initial='23:30')
    gender = forms.ChoiceField(choices=ProfileModel.GENDERS)
    ip_address = forms.GenericIPAddressField(initial='59.192.223.180')
    slug = forms.SlugField(initial='testslug')
    website = forms.URLField(initial='http://test.com')

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
