from django.contrib import admin
from .models import Shop, VendorDocument


@admin.register(Shop)
class ShopAdmin(admin.ModelAdmin):
    list_display = ['name', 'vendor', 'status', 'is_active', 'created_at']
    list_filter = ['status', 'is_active', 'created_at']
    search_fields = ['name', 'vendor__username', 'gstin']
    ordering = ['-created_at']


@admin.register(VendorDocument)
class VendorDocumentAdmin(admin.ModelAdmin):
    list_display = ['vendor', 'doc_type', 'verified', 'uploaded_at']
    list_filter = ['doc_type', 'verified']
    search_fields = ['vendor__username']
    ordering = ['-uploaded_at']
