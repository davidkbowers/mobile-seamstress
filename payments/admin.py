from django.contrib import admin
from .models import Payment


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('customer', 'amount', 'date', 'payment_method', 'status', 'created_by')
    list_filter = ('status', 'payment_method', 'date', 'created_by')
    search_fields = ('customer__name', 'notes')
    readonly_fields = ('created_at', 'updated_at')
    
    def save_model(self, request, obj, form, change):
        if not change:  # Creating new object
            obj.created_by = request.user
        super().save_model(request, obj, form, change)
