from django.contrib import admin
from .models import Reservation


@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = ('pk', 'user', 'facility', 'check_in', 'check_out', 'status', 'total_price')
    list_filter = ('status', 'facility', 'check_in')
    search_fields = ('user__username', 'user__email', 'facility__name')
    readonly_fields = ('created_at', 'updated_at')
    date_hierarchy = 'check_in'
