# -*- coding: utf-8 -*-

from django import forms
from django.conf import settings
from django.forms import widgets
from django.template.loader import render_to_string
from django.utils.safestring import mark_safe

"""
Copied this from djplaces package to specify the google maps js language (added &language=en).

"""


class LocationWidget(widgets.TextInput):
    def render(self, name, value, attrs=None):
        text_input = super(LocationWidget, self).render(name, value, attrs)

        return render_to_string('djplaces/map_widget.html', {
            'field_name': name,
            'field_input': mark_safe(text_input)
        })

    def _media(self):
        return forms.Media(
            css={'all': ('css/djplaces.css',)},
            js=(
                '//cdnjs.cloudflare.com/ajax/libs/jquery/2.2.0/jquery.min.js',
                '//maps.googleapis.com/maps/api/js?key=' + settings.MAPS_API_KEY + '&libraries=places&language=en',
                '//cdnjs.cloudflare.com/ajax/libs/geocomplete/1.7.0/jquery.geocomplete.js',
                'js/djplaces.js',
            )
        )

    media = property(_media)
