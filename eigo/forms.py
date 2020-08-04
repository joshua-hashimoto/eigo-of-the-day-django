from django import forms
from django.forms.models import inlineformset_factory
from martor.fields import MartorFormField

from .models import Phrase, Example, Snap


class PhraseForm(forms.ModelForm):

    class Meta:
        model = Phrase
        fields = ('phrase', )


class ExampleForm(forms.ModelForm):

    class Meta:
        model = Example
        fields = ('example',)


class SnapForm(forms.ModelForm):

    class Meta:
        model = Snap
        fields = ('snap',)


ExampleFormSet = inlineformset_factory(
    Phrase,
    Example,
    form=ExampleForm,
    fields=['example', ],
    extra=3,
    can_delete=False,
)

SnapFormSet = inlineformset_factory(
    Phrase,
    Snap,
    form=SnapForm,
    fields=['snap', ],
    extra=5,
    can_delete=False,
)
