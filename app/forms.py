from django import forms
from s3direct.widgets import S3DirectWidget

from app.models import Item


class MyForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.add_class()

    def add_class(self):
        for f in self.fields.values():
            w = f.widget
            w.attrs.update({'class': 'form-control'})


class ItemForm(MyForm):
    class Meta:
        model = Item
        exclude = [
            'user',
            'renters',
            'published',
        ]

        widgets = {
            'categories': forms.CheckboxSelectMultiple()
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['location'].widget.attrs['readonly'] = True
        for f in self.fields.values():
            w = f.widget
            w.attrs.update({'title': 'tooltip text'})


class S3DirectUploadForm(forms.Form):
    image01 = forms.URLField(widget=S3DirectWidget(dest='images_destination'))
    image02 = forms.URLField(widget=S3DirectWidget(dest='images_destination'),  required=False)
    image03 = forms.URLField(widget=S3DirectWidget(dest='images_destination'),  required=False)
    image04 = forms.URLField(widget=S3DirectWidget(dest='images_destination'),  required=False)
    image05 = forms.URLField(widget=S3DirectWidget(dest='images_destination'),  required=False)
    image06 = forms.URLField(widget=S3DirectWidget(dest='images_destination'),  required=False)
    image07 = forms.URLField(widget=S3DirectWidget(dest='images_destination'),  required=False)
    image08 = forms.URLField(widget=S3DirectWidget(dest='images_destination'),  required=False)
    image09 = forms.URLField(widget=S3DirectWidget(dest='images_destination'),  required=False)
    image10 = forms.URLField(widget=S3DirectWidget(dest='images_destination'),  required=False)

    def add_class(self):
        for f in self.fields.values():
            w = f.widget
            w.attrs.update({'class': 'form-control'})

