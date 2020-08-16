from django import forms
from extra_views import InlineFormSetFactory


from .models import Example, Snap


class ExampleInlineFormSet(InlineFormSetFactory):
    """
    inlineformset class using django-extra-views.

    Attributes:
        model (Example): model to create an inlineformset_factory
        fields (Tuple): model fields that will be rendered in the template
        prefix (str): set prefix that will be use in the rendered forms in the template.
        factory_kwargs (Dict): a dictionary to set additional information for inlineformset_factory.
    """
    model = Example
    fields = ('example',)
    prefix = 'example-form'
    factory_kwargs = {'extra': 3, 'max_num': None,
                      'can_order': False, 'can_delete': True}


class SnapInlineFormSet(InlineFormSetFactory):
    """
    inlineformset class using django-extra-views.

    Attributes:
        model (Snap): model to create an inlineformset_factory
        fields (Tuple): model fields that will be rendered in the template
        prefix (str): set prefix that will be use in the rendered forms in the template.
        factory_kwargs (Dict): a dictionary to set additional information for inlineformset_factory.
    """
    model = Snap
    fields = ('snap',)
    prefix = 'snap-form'
    factory_kwargs = {'extra': 5, 'max_num': None,
                      'can_order': False, 'can_delete': True}
