import django_filters
from .models import MyModel4


class MyModel4Filter(django_filters.FilterSet):
    hair_color = django_filters.ChoiceFilter(
        field_name='hair_color',
        choices=MyModel4.HairColor.choices,
        null_label='Any',
        label='Hair Color',
    )

    my_model3__hair_length_cm__range = django_filters.RangeFilter(
        field_name='my_model3__hair_length_cm',
        label='Hair Length (Range)',
    )

    my_model1__name__icontains = django_filters.CharFilter(
        field_name='my_model1__name',
        lookup_expr='icontains',
        label='Name (Contains)',
    )

    my_model1__age__range = django_filters.RangeFilter(
        field_name='my_model1__age',
        label='Age (Range)',
    )

    my_model1__dob__range = django_filters.DateFromToRangeFilter(
        field_name='my_model1__dob',
        label='DOB (Date Range)',
    )

    class Meta:
        model = MyModel4
        fields = {
            'hair_color': ['exact'],
            'my_model3__hair_length_cm': ['range'],
            'my_model1__name': ['icontains'],
            'my_model1__age': ['range'],
            'my_model1__dob': ['range'],
        }
