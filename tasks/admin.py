from django.contrib import admin

from .models import Task


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'owner',
        'status',
        'due_date',
        'lead',
        'contact',
        'updated_at',
    )
    list_filter = ('status', 'due_date', 'created_at')
    search_fields = ('title', 'description', 'lead__name', 'contact__name')
    autocomplete_fields = ('owner', 'lead', 'contact')
    date_hierarchy = 'due_date'
