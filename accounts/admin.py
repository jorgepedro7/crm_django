from django.contrib import admin

from leads.models import Lead

from .models import Account


class LeadInline(admin.TabularInline):
    model = Lead
    fields = ('name', 'email', 'status', 'source')
    readonly_fields = ('name', 'email', 'status', 'source')
    can_delete = False
    extra = 0
    show_change_link = True


@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = ['name', 'industry', 'city', 'owner', 'created_at']
    list_filter = ['industry', 'city', 'created_at']
    search_fields = ['name', 'industry', 'city', 'owner__email']
    autocomplete_fields = ['owner']
    inlines = [LeadInline]
