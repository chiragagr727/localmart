from django.contrib import admin
from .models import Order, OrderItem


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'customer', 'status', 'payment_mode', 'total', 'created_at']
    list_filter = ['status', 'payment_mode', 'created_at']
    search_fields = ['id', 'customer__username']
    ordering = ['-created_at']
    inlines = [OrderItemInline]
