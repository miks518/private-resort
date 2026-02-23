from django.contrib import admin
from .models import Payment


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('pk', 'user', 'reservation', 'amount', 'payment_method', 'status', 'paid_at')
    list_filter = ('status', 'payment_method')
    search_fields = ('user__username', 'receipt_number', 'paymongo_checkout_id')
    readonly_fields = ('created_at', 'updated_at')
