from django.contrib import admin
from .models import Vendor


@admin.register(Vendor)
class VendorAdmin(admin.ModelAdmin):
    """
    Admin interface for Vendor model.
    """
    list_display = ('name', 'vendor_score', 'delivery_rating', 'quality_rating', 'price_rating', 'communication_rating', 'created_at')
    list_filter = ('created_at', 'updated_at')
    search_fields = ('name',)
    readonly_fields = ('created_at', 'updated_at', 'vendor_score')
    
    fieldsets = (
        ('Vendor Information', {
            'fields': ('name',)
        }),
        ('Performance Ratings (1-5 scale)', {
            'fields': ('delivery_rating', 'quality_rating', 'price_rating', 'communication_rating')
        }),
        ('Calculated Score', {
            'fields': ('vendor_score',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def vendor_score(self, obj):
        """Display vendor score in list view."""
        return f"{obj.vendor_score()}/5.0"
    vendor_score.short_description = 'Overall Score'
