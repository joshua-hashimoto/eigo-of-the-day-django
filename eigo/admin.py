from django.contrib import admin
from django.db import models

from .models import Phrase, Example, Snap


class ExampleInline(admin.TabularInline):
    """
    Attributes:
        model (Example): set model Example for TabularInline
    """
    model = Example


class SnapInline(admin.TabularInline):
    """
    Attributes:
        model (Snap): set model Snap for TabularInline
    """
    model = Snap


class PhraseAdmin(admin.ModelAdmin):
    """
    custom admin for model Phrase

    Attributes:
        list_desplay (List): list of fields in model to display in admin site.
        list_display_links (List): list of fields in model to attach links to in admin site.
        list_filter (List): list of fields in model that the user can filter through in admin site.
        search_fields (List): list of fields in model that the user can search through in admin site.
        actions (List): list of custom functions to add custom actions to admin site.
        inlines (List): list of custom Inline classes to add relational fields in admin site.
    """

    list_display = [
        'id',
        'phrase',
        'examples',
        'snaps',
        'is_active',
    ]
    list_display_links = [
        'id',
    ]
    list_filter = [
        'phrase',
        'is_active',
    ]
    search_fields = [
        'phrase',
    ]
    actions = ['active', 'inactive']
    inlines = [
        ExampleInline,
        SnapInline,
    ]

    def active(self, request, queryset):
        """
        function to set the target model's "is_active" to True.
        used in admin site.
        """
        queryset.update(is_active=True)

    active.short_description = '閲覧可能'

    def inactive(self, request, queryset):
        """
        function to set the target model's "is_active" to False.
        used in admin site.
        """
        queryset.update(is_active=False)

    inactive.short_description = '閲覧不可能'

    def examples(self, obj):
        """
        custom admin column.
        count how many examples are tied to the phrase.

        Args:
            obj (Phrase): data object.

        Returns:
            int: number of examples related to the object
        """
        return obj.examples.count()

    examples.short_description = 'examples'

    def snaps(self, obj):
        """
        custom admin column.
        count how many snaps are tied to the phrase.

        Args:
            obj (Phrase): data object.

        Returns:
            int: number of snaps related to the object
        """
        return obj.snaps.count()

    snaps.short_description = 'snaps'


class SnapAdmin(admin.ModelAdmin):
    """
    custom admin for model Snap

    Attributes:
        list_desplay (List): list of fields in model to display in admin site.
        list_display_links (List): list of fields in model to attach links to in admin site.
        list_filter (List): list of fields in model that the user can filter through in admin site.
    """
    list_display = [
        'id',
        'snap',
        'is_active',
    ]
    list_display_links = [
        'id',
    ]
    list_filter = [
        'snap',
        'is_active',
    ]


admin.site.register(Phrase, PhraseAdmin)
admin.site.register(Example)
admin.site.register(Snap, SnapAdmin)
