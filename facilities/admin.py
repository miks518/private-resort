from django.contrib import admin
from .models import Facility, FacilityImage, VirtualTour


class FacilityImageInline(admin.TabularInline):
    model = FacilityImage
    extra = 1


class VirtualTourInline(admin.TabularInline):
    model = VirtualTour
    extra = 1


@admin.register(Facility)
class FacilityAdmin(admin.ModelAdmin):
    list_display = ('name', 'capacity', 'price_per_day', 'is_available')
    list_filter = ('is_available',)
    search_fields = ('name', 'description')
    prepopulated_fields = {'slug': ('name',)}
    inlines = [FacilityImageInline, VirtualTourInline]


@admin.register(VirtualTour)
class VirtualTourAdmin(admin.ModelAdmin):
    list_display = ('title', 'facility', 'media_type', 'order')
    list_filter = ('media_type', 'facility')
