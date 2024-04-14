from django import template
import random

register = template.Library()


@register.filter
def phone_number(value, sep):
    """
    filter accepts only one argument
    """
    if value.raw_input:
        return f"{value.raw_input[:3]} {value.raw_input[3:6]}{sep}{value.raw_input[6:9]}{sep}{value.raw_input[9:]}"

    return value


@register.simple_tag
def random_number(min_num, max_num):
    """
    use {% random_number 1 100 %} in your html
    """
    return random.randint(min_num, max_num)
