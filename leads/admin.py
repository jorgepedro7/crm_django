from django.contrib import admin

from .models import Lead


@admin.register(Lead)
class LeadAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'email',
        'status',
        'source',
        'owner',
        'account',
        'contact',
        'updated_at',
    )
    list_filter = ('status', 'source', 'created_at')
    search_fields = ('name', 'email', 'phone', 'account__name')
    autocomplete_fields = ('owner', 'account', 'contact')
    readonly_fields = ('created_at', 'updated_at')
