from django.utils.safestring import mark_safe
from django_tables2 import tables

from app.models import Item


class ItemTable(tables.Table):
    def render_name(self, record):
        return mark_safe('<a href=%s>%s</a>' % (
            record.get_absolute_url(),
            record.name
        ))

    class Meta:
        model = Item
        exclude = (
            'id',
            'description',
            'location',
            'user',
            'is_published',
        )
        # sequence = (
        #     'name',
        #     'phone_number',
        #     'email',
        # )
        order_by = ('name',)
        attrs = {"class": "paleblue"}
