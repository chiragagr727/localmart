from django.db import models
from django.conf import settings
import uuid


class Shop(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending Approval'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('suspended', 'Suspended'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    vendor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='shops')
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    images = models.JSONField(default=list, blank=True)  # store list of image URLs/paths
    gstin = models.CharField(max_length=20, blank=True, null=True)
    fssai = models.CharField(max_length=20, blank=True, null=True)
    pan = models.CharField(max_length=20, blank=True, null=True)
    apob = models.CharField(max_length=50, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    location = models.JSONField(blank=True, null=True)  # { lat, lng }
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    is_active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'shops'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} ({self.vendor.username})"


class VendorDocument(models.Model):
    DOC_TYPES = [
        ('gstin', 'GSTIN'),
        ('pan', 'PAN'),
        ('fssai', 'FSSAI'),
        ('apob', 'APOB'),
        ('other', 'Other'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    vendor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='vendor_documents')
    doc_type = models.CharField(max_length=20, choices=DOC_TYPES)
    document = models.FileField(upload_to='kyc_documents/')
    verified = models.BooleanField(default=False)
    remarks = models.TextField(blank=True, null=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'vendor_documents'
        ordering = ['-uploaded_at']

    def __str__(self):
        return f"{self.vendor.username} - {self.doc_type}"
