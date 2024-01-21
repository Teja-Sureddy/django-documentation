import django_tables2 as tables
from .models import MyModel4
from django.utils.html import format_html, escape
from django.utils.safestring import mark_safe
from datetime import datetime


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


class MyModel4Table(tables.Table):
    class Meta:
        model = MyModel4
        template_name = 'django_tables2/bootstrap4.html'
        attrs = {'class': 'table table-bordered table-hover table-light mb-0'}
        exclude = ('id', 'json_data', 'my_model1', 'my_model2', 'my_model3')

    hair_color = tables.Column()
    duration = tables.Column()

    is_hair_styled = tables.Column(accessor='my_model3.is_hair_styled', verbose_name='Is Hair Styled')
    hair_length_cm = tables.Column(accessor='my_model3.hair_length_cm', verbose_name='Hair Length (cm)')
    hair_color_intensity = tables.Column(accessor='my_model3.hair_color_intensity', verbose_name='Hair Color Intensity')
    hair_shine_factor = tables.Column(accessor='my_model3.hair_shine_factor', verbose_name='Hair Shine Factor')
    hair_description = tables.Column(accessor='my_model3.hair_description', verbose_name='Hair Description')

    favorite_colors = tables.Column(accessor='my_model2.all', verbose_name='Favorite Colors')

    name = tables.Column(accessor='my_model1.name', verbose_name='Name')
    email = tables.Column(accessor='my_model1.email', verbose_name='Email')
    age = tables.Column(accessor='my_model1.age', verbose_name='Age')
    dob_tob = tables.Column(verbose_name='DOB & TOB', empty_values=())
    gender = tables.Column(accessor='my_model1.gender', verbose_name='Gender')
    ip_address = tables.Column(accessor='my_model1.ip_address', verbose_name='IP Address')
    slug = tables.Column(accessor='my_model1.slug', verbose_name='Slug')
    website = tables.Column(accessor='my_model1.website', verbose_name='Website')
    identity = tables.Column(accessor='my_model1.identity', verbose_name='Identity')
    created_at = tables.Column(accessor='my_model1.created_at', verbose_name='Created At')
    updated_at = tables.Column(accessor='my_model1.updated_at', verbose_name='Updated At')

    actions = tables.TemplateColumn(
        template_code='''<a href="#" class="text-primary me-1 py-1">Edit</a>
                         <a href="#" class="text-danger ms-1 py-1">Delete</a>''',
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
        dob = record.my_model1.dob
        tob = record.my_model1.tob
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
