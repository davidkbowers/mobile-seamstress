from django.contrib import admin
from .models import Job


@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = ('customer', 'description_short', 'due_date', 'status', 'created_at', 'created_by')
    list_filter = ('status', 'due_date', 'created_at', 'created_by')
    search_fields = ('customer__name', 'description', 'notes')
    readonly_fields = ('created_at', 'updated_at')
    
    def description_short(self, obj):
        return obj.description[:50] + '...' if len(obj.description) > 50 else obj.description
    description_short.short_description = 'Description'
    
    def save_model(self, request, obj, form, change):
        if not change:  # Creating new object
            obj.created_by = request.user
        super().save_model(request, obj, form, change)
