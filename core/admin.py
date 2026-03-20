from django.contrib import admin
from .models import RatePackage


@admin.register(RatePackage)
class RatePackageAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'order')
    ordering = ('order', 'name')
    list_editable = ('price', 'order')
