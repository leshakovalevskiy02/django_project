from django import template

register = template.Library()


@register.filter
def swapcase(string: str):
    return string.swapcase()


@register.filter(name="email")
def add_email_to_string(string, mail):
    return string + "@" + mail