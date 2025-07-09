from django import template

register = template.Library()


@register.filter
def swapcase(string: str):
    return string.swapcase()


@register.filter(name="email")
def add_email_to_string(string, mail):
    return string + "@" + mail

@register.filter
def pluralize_ru(number, variants):
    variants = variants.split(',')
    number = abs(number)

    if number % 10 == 1 and number % 100 != 11:
        variant = 0
    elif 2 <= number % 10 <= 4 and number % 100 not in (12, 13, 14):
        variant = 1
    else:
        variant = 2

    return variants[variant]