from django.contrib import admin

from .models import Account


@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = ['name', 'industry', 'city', 'owner', 'created_at']
    list_filter = ['industry', 'city', 'created_at']
    search_fields = ['name', 'industry', 'city', 'owner__email']
    autocomplete_fields = ['owner']
