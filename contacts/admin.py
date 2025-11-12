from django.contrib import admin

from leads.models import Lead

from .models import Contact


class LeadInline(admin.TabularInline):
    model = Lead
    fields = ('name', 'email', 'status', 'source')
    readonly_fields = ('name', 'email', 'status', 'source')
    can_delete = False
    extra = 0
    show_change_link = True


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'account',
        'owner',
        'email',
        'phone',
        'updated_at',
    )
    list_filter = ('account',)
    search_fields = ('name', 'email', 'phone')
    autocomplete_fields = ('account',)
    inlines = [LeadInline]
