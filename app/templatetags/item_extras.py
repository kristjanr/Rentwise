from django import template
from app.models import Item


def verbose_name(fieldname):
    return Item._meta.get_field(fieldname).verbose_name  # put here whatever you would like to return

register = template.Library()

verbose_name = register.filter(verbose_name)
