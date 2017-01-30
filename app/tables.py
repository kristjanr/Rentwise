from django.utils.safestring import mark_safe
from django_tables2 import Column
from django_tables2 import Table

from app.models import FoundItem
from app.models import Item


class ItemTable(Table):
    """
    Table used in search results when no location was entered during search.
    """
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
            'email_sent_to_user',
        )
        order_by = ('-created_at',)
        attrs = {'class': 'paleblue'}


class FoundItemTable(Table):
    """
    Table used in search results when a location was entered during search.
    """
    name = Column(accessor='item.name')
    price_per_day = Column(accessor='item.price_per_day')
    minimum_rental_period = Column(accessor='item.minimum_rental_period')
    estimated_value = Column(accessor='item.estimated_value')
    created_at = Column(accessor='item.created_at')

    def render_name(self, record):
        return mark_safe('<a href=%s?distance=%f>%s</a>' % (
            record.item.get_absolute_url(),
            record.distance,
            record.item.name
        ))

    def render_distance(self, value):
        return '%.2f' % value

    class Meta:
        model = FoundItem
        exclude = (
            'id',
            'item',
            'search',
            'user',
            'is_created',
        )

        sequence = (
            'name',
            'price_per_day',
            'minimum_rental_period',
            'estimated_value',
            'created_at',
            'distance',
        )
        order_by = ('-created_at',)
        attrs = {"class": "paleblue"}
