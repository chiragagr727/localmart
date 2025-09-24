from rest_framework import serializers
from .models import Shop, VendorDocument


class VendorDocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = VendorDocument
        fields = ['id', 'doc_type', 'document', 'verified', 'remarks', 'uploaded_at']
        read_only_fields = ['id', 'verified', 'uploaded_at']


class ShopSerializer(serializers.ModelSerializer):
    vendor_id = serializers.UUIDField(source='vendor.id', read_only=True)

    class Meta:
        model = Shop
        fields = [
            'id', 'vendor_id', 'name', 'description', 'images', 'gstin', 'fssai', 'pan', 'apob',
            'address', 'location', 'status', 'is_active', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'status', 'is_active', 'created_at', 'updated_at', 'vendor_id']

    def create(self, validated_data):
        validated_data['vendor'] = self.context['request'].user
        return super().create(validated_data)
