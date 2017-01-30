from django import template
from app.models import Item


def verbose_name(fieldname):
    """
    Returns Item's verbose_name of the given fieldname.
    """
    return Item._meta.get_field(fieldname).verbose_name

register = template.Library()

verbose_name = register.filter(verbose_name)
