from django import template

register = template.Library()


@register.filter(name="add_attrs")
def add_attrs(field, args):
    attrs = {}

    for attr in args.split('; '):
        key, value = attr.split("=")
        attrs[key.strip()] = value.strip()

    return field.as_widget(attrs=attrs)
