from django import template

register = template.Library()

@register.filter
def multiply(value, arg):
    """Multiply the arg by the value."""
    try:
        return int(value) * int(arg)
    except (ValueError, TypeError):
        return ''

@register.filter
def divisibleby(value, arg):
    """Check if value is divisible by arg and return index to use for delays."""
    try:
        remainder = int(value) % int(arg)
        return remainder
    except (ValueError, TypeError):
        return 0
