import django_filters
import django_tables2 as tables
from my_apps.dashboard.models import FullDataModel
from django.utils.html import format_html, escape
from django.utils.safestring import mark_safe
from datetime import datetime
from django import forms


# Table
def website_linkify(link):
    if link:
        return format_html('<a href="{}" target="_blank">{}</a>', escape(link), escape(link))
    return ''


def format_datetime(value):
    if value:
        if type(value) == str:
            value = datetime.strptime(value, '%Y-%m-%d %H:%M %p')
        formatted_date = value.strftime('%b %d, %Y, %I:%M %p')
        return format_html('<span title="{}">{}</span>', formatted_date, formatted_date)
    return ''


class FullDataTable(tables.Table):
    class Meta:
        model = FullDataModel
        template_name = 'django_tables2/bootstrap4.html'
        attrs = {'class': 'table table-hover table-white mb-0'}
        exclude = ('id', 'json_data', 'data', 'color', 'hair')
        sequence = ('name', 'email', 'age', 'dob_tob', 'gender', 'ip_address', 'slug', 'website', 'identity',
                    'hair_color', 'duration', 'is_hair_styled', 'hair_length_cm', 'hair_color_intensity',
                    'hair_shine_factor', 'hair_description', 'favorite_colors', 'created_at', 'updated_at', 'actions')
        default = ''

    hair_color = tables.Column()
    duration = tables.Column()

    is_hair_styled = tables.Column(accessor='hair.is_hair_styled', verbose_name='Is Hair Styled')
    hair_length_cm = tables.Column(accessor='hair.hair_length_cm', verbose_name='Hair Length (cm)')
    hair_color_intensity = tables.Column(accessor='hair.hair_color_intensity', verbose_name='Hair Color Intensity')
    hair_shine_factor = tables.Column(accessor='hair.hair_shine_factor', verbose_name='Hair Shine Factor')
    hair_description = tables.Column(accessor='hair.hair_description', verbose_name='Hair Description')

    favorite_colors = tables.Column(accessor='color.all', verbose_name='Favorite Colors')

    name = tables.Column(accessor='data.name', verbose_name='Name')
    email = tables.Column(accessor='data.email', verbose_name='Email')
    age = tables.Column(accessor='data.age', verbose_name='Age')
    dob_tob = tables.Column(verbose_name='DOB & TOB', empty_values=())
    gender = tables.Column(accessor='data.gender', verbose_name='Gender')
    ip_address = tables.Column(accessor='data.ip_address', verbose_name='IP Address')
    slug = tables.Column(accessor='data.slug', verbose_name='Slug')
    website = tables.Column(accessor='data.website', verbose_name='Website')
    identity = tables.Column(accessor='data.identity', verbose_name='Identity')
    created_at = tables.Column(accessor='data.created_at', verbose_name='Created At')
    updated_at = tables.Column(accessor='data.updated_at', verbose_name='Updated At')

    actions = tables.TemplateColumn(
        template_code='''<a href="{% url 'dashboard:data-edit' pk=record.id %}" class="text-primary me-1 py-1">Edit</a>
                         <a href="#" data-bs-toggle="modal" data-bs-target="#deleteModel" data-pk="{{ record.id }}" 
                         class="text-danger ms-1 py-1">Delete</a>''',
        verbose_name='Actions',
        orderable=False
    )

    @staticmethod
    def render_hair_color(value):
        color_mapping = {'Blonde': 'b38b67', 'Brown': '964B00', 'Black': '000', 'Red': 'e1621d', 'Other': 'b4b4b4'}

        if value in color_mapping:
            color_class = color_mapping[value]
            return format_html('<span style="background-color: #{0};" class="badge">{1}</span>', color_class, value)
        return ''

    @staticmethod
    def render_is_hair_styled(value):
        if value:
            return format_html('<span style="color: green; font-size: larger;">&#10004;</span>')
        return format_html('<span style="color: red; font-size: larger;">&#10008;</span>')

    @staticmethod
    def render_email(value):
        if value:
            email_link = format_html('<a href="mailto:{}">{}</a>', value, value)
            return mark_safe(email_link)
        return ''

    @staticmethod
    def render_dob_tob(record):
        dob = record.data.dob
        tob = record.data.tob
        if dob and tob:
            formatted_dob_tob = format_html('{} {}', dob.strftime('%Y-%m-%d'), tob.strftime('%H:%M %p'))
            return format_datetime(str.__str__(formatted_dob_tob))
        return ''

    @staticmethod
    def render_gender(value):
        if value:
            symbol_mapping = {'Male': '♂', 'Female': '♀'}
            symbol = symbol_mapping.get(value, value)
            return format_html('<span title="{}">{}</span>', value, symbol)
        return ''

    @staticmethod
    def render_hair_shine_factor(value):
        if value is not None:
            rounded_value = round(value, 10)
            return '{:.10f}'.format(rounded_value)
        return ''

    @staticmethod
    def render_favorite_colors(value):
        return ', '.join(str(color) for color in value.all())

    @staticmethod
    def render_website(value):
        return website_linkify(value)

    @staticmethod
    def render_created_at(value):
        return format_datetime(value)

    @staticmethod
    def render_updated_at(value):
        return format_datetime(value)


# Filter
class CustomRangeWidget(django_filters.widgets.RangeWidget):
    def __init__(self, attrs=None):
        super().__init__(attrs)
        self.widgets[0].attrs.update({'placeholder': attrs.get('ph1'), 'class': 'me-2'})
        self.widgets[1].attrs.update({'placeholder': attrs.get('ph2'), 'class': 'ms-2'})

    def render(self, name, value, attrs=None, renderer=None):
        html = '<div class="range-inputs">'
        html += super().render(name, value, attrs, renderer)
        html += '</div>'
        return html


class FullDataFilter(django_filters.FilterSet):
    class Meta:
        model = FullDataModel
        fields = {
            'data__name': ['icontains'],
            'data__age': ['range'],
            'data__dob': ['range'],
            'hair_color': ['exact'],
            'hair__hair_length_cm': ['range'],
        }

    data__name__icontains = django_filters.CharFilter(
        field_name='data__name',
        lookup_expr='icontains',
        label='Enter name',
        widget=forms.TextInput(attrs={'placeholder': 'Name'}),
    )

    data__age__range = django_filters.RangeFilter(
        field_name='data__age',
        label='Age',
        widget=CustomRangeWidget({'ph1': 'Min age', 'ph2': 'Max age'})
    )

    data__dob__range = django_filters.DateFromToRangeFilter(
        field_name='data__dob',
        label='Date of birth',
        widget=CustomRangeWidget({'ph1': 'Min YYYY-MM-DD', 'ph2': 'Max YYYY-MM-DD'})
    )

    hair_color = django_filters.ChoiceFilter(
        field_name='hair_color',
        choices=FullDataModel.HairColor.choices,
        label='Hair Color',
        empty_label='Select hair color'
    )

    hair__hair_length_cm__range = django_filters.RangeFilter(
        field_name='hair__hair_length_cm',
        label='Hair Length',
        widget=CustomRangeWidget({'ph1': 'Min length', 'ph2': 'Max length'})
    )


def set_dropdown_attrs(fields):
    for key, value in fields.items():
        if type(value) in (forms.ChoiceField, forms.ModelChoiceField,
                           forms.TypedChoiceField, forms.ModelMultipleChoiceField):
            value.widget.attrs['class'] = 'd-none select2'
