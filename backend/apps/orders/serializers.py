from rest_framework import serializers
from .models import Order, OrderItem


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ['id', 'product', 'quantity', 'price']
        read_only_fields = ['id']


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True)

    class Meta:
        model = Order
        fields = [
            'id', 'customer', 'delivery_partner', 'status', 'payment_mode',
            'shipping_address', 'subtotal', 'delivery_fee', 'discount', 'total',
            'notes', 'created_at', 'updated_at', 'items'
        ]
        read_only_fields = ['id', 'status', 'customer', 'subtotal', 'total', 'created_at', 'updated_at']

    def create(self, validated_data):
        items_data = validated_data.pop('items', [])
        validated_data['customer'] = self.context['request'].user
        order = Order.objects.create(**validated_data)
        subtotal = 0
        for item in items_data:
            OrderItem.objects.create(order=order, **item)
            subtotal += item['price'] * item['quantity']
        order.subtotal = subtotal
        order.total = subtotal + order.delivery_fee - order.discount
        order.save()
        return order
