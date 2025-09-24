from rest_framework import serializers
from .models import Category, Product


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'parent']


class ProductSerializer(serializers.ModelSerializer):
    shop_id = serializers.UUIDField(source='shop.id', read_only=True)

    class Meta:
        model = Product
        fields = [
            'id', 'shop_id', 'name', 'description', 'images', 'price', 'mrp',
            'category', 'stock', 'is_active', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'shop_id', 'created_at', 'updated_at']
