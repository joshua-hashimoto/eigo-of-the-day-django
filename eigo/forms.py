from django import forms
from extra_views import InlineFormSetFactory


from .models import Example, Snap


class ExampleInlineFormSet(InlineFormSetFactory):
    model = Example
    fields = ('example',)
    prefix = 'example-form'
    factory_kwargs = {'extra': 3, 'max_num': None,
                      'can_order': False, 'can_delete': False}


class SnapInlineFormSet(InlineFormSetFactory):
    model = Snap
    fields = ('snap',)
    prefix = 'snap-form'
    factory_kwargs = {'extra': 5, 'max_num': None,
                      'can_order': False, 'can_delete': False}
