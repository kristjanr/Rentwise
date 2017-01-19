from django import forms
from s3direct.widgets import S3DirectWidget

from app.models import Item, Search


class MyForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.add_class()

    def add_class(self):
        for f in self.fields.values():
            w = f.widget
            w.attrs.update({
                'class': 'form-control',
                'data-toggle': 'tooltip',
            })


class S3DirectUploadForm(forms.Form):
    image01 = forms.URLField(widget=S3DirectWidget(dest='images_destination'))
    image02 = forms.URLField(widget=S3DirectWidget(dest='images_destination'), required=False)
    image03 = forms.URLField(widget=S3DirectWidget(dest='images_destination'), required=False)
    image04 = forms.URLField(widget=S3DirectWidget(dest='images_destination'), required=False)
    image05 = forms.URLField(widget=S3DirectWidget(dest='images_destination'), required=False)
    image06 = forms.URLField(widget=S3DirectWidget(dest='images_destination'), required=False)
    image07 = forms.URLField(widget=S3DirectWidget(dest='images_destination'), required=False)
    image08 = forms.URLField(widget=S3DirectWidget(dest='images_destination'), required=False)
    image09 = forms.URLField(widget=S3DirectWidget(dest='images_destination'), required=False)
    image10 = forms.URLField(widget=S3DirectWidget(dest='images_destination'), required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for f in self.fields.values():
            w = f.widget
            w.attrs.update({
                'class': 'form-control',
            })


tooltips = {
    'name': 'This will be the title for your item.',
    'description': 'This is going to appear in the detailed view of your item. Describe the item in as much detail as you think is necessary and try to make it as attractive as possible.',
    'price_per_day': 'This is the price you plan to charge per one day.',
    'minimum_rental_period': 'This is the minimum number of days you are willing to rent your item out for.',
    'estimated_value': 'This is the estimated value of your item. This can be used as a legal basis in case of any problems. Stay realistic!',
    'place': 'This is the location, where you are renting out your item.',
}


class ItemForm(MyForm, S3DirectUploadForm):
    class Meta:
        model = Item
        exclude = [
            'user',
            'renters',
            'is_published',
        ]

        widgets = {
            'categories': forms.CheckboxSelectMultiple()
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['location'].widget.attrs['readonly'] = True
        self.fields['location'].widget.attrs['style'] = 'display:none;'
        for field_name, tooltip in tooltips.items():
            f = self.fields[field_name]
            w = f.widget
            w.attrs.update({'title': tooltip})


class SearchForm(forms.ModelForm):
    class Meta:
        model = Search
        fields = [
            'what',
            'place',
            'location',
            'category',
        ]
