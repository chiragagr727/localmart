from django.contrib import admin
from .models import Category, Product


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'parent']
    search_fields = ['name']


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'shop', 'price', 'stock', 'is_active', 'created_at']
    list_filter = ['is_active', 'created_at', 'category']
    search_fields = ['name', 'shop__name']
    ordering = ['-created_at']
