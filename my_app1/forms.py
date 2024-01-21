# forms.py
from django import forms
from .models import MyModel4, MyModel1


class MyModel4Form(forms.ModelForm):
    class Meta:
        model = MyModel4
        fields = ['hair_color', 'duration', 'json_data', 'my_model2', 'my_model3']

    name = forms.CharField(max_length=100, initial='Person')
    email = forms.EmailField(initial='Persontest@gmail.com')
    age = forms.IntegerField(initial=22)
    dob = forms.DateField(initial='2024-12-12')
    tob = forms.TimeField(initial='23:30')
    gender = forms.ChoiceField(choices=MyModel1.GENDERS)
    ip_address = forms.GenericIPAddressField(initial='59.192.223.180')
    slug = forms.SlugField(initial='testslug')
    website = forms.URLField(initial='http://test.com')

    def save(self, commit=True):
        my_model1_data = {
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
        my_model1 = MyModel1.objects.create(**my_model1_data)
        self.cleaned_data['my_model1'] = my_model1
        self.instance.my_model1 = my_model1
        my_model4 = super().save(commit=commit)
        my_model4.my_model2.set(self.cleaned_data['my_model2'])
        return my_model4
