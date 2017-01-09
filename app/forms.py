from django import forms

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
            'profile',
            'renters',
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
