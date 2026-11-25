from django.contrib import admin
from .models import Crop, CropListing


@admin.register(Crop)
class CropAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'updated_at')
    list_filter = ('category',)
    search_fields = ('name',)


@admin.register(CropListing)
class CropListingAdmin(admin.ModelAdmin):
    list_display = ('crop', 'farmer', 'quantity', 'unit', 'availability_status', 'state', 'district')
    list_filter = ('availability_status', 'state', 'unit')
    search_fields = ('crop__name', 'farmer__user__username', 'district')
