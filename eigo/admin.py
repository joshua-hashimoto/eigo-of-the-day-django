from django.contrib import admin
from django.db import models

from .models import Phrase, Example, Snap


class ExampleInline(admin.TabularInline):
    """
    Attributes:
    """
    model = Example


class SnapInline(admin.TabularInline):
    model = Snap


class PhraseAdmin(admin.ModelAdmin):

    list_display = [
        'id',
        'phrase',
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


class SnapAdmin(admin.ModelAdmin):
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
