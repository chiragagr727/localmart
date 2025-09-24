from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, UserAddress, OTPVerification, UserWallet, WalletTransaction


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """Custom User admin"""
    list_display = ['username', 'email', 'phone', 'role', 'status', 'is_active', 'created_at']
    list_filter = ['role', 'status', 'is_active', 'is_phone_verified', 'is_email_verified']
    search_fields = ['username', 'email', 'phone', 'first_name', 'last_name']
    ordering = ['-created_at']
    
    fieldsets = BaseUserAdmin.fieldsets + (
        ('Additional Info', {
            'fields': ('role', 'phone', 'date_of_birth', 'gender', 'status', 
                      'profile_picture', 'is_phone_verified', 'is_email_verified',
                      'fcm_token', 'last_location')
        }),
    )
    
    add_fieldsets = BaseUserAdmin.add_fieldsets + (
        ('Additional Info', {
            'fields': ('role', 'phone', 'email')
        }),
    )


@admin.register(UserAddress)
class UserAddressAdmin(admin.ModelAdmin):
    """User Address admin"""
    list_display = ['user', 'address_type', 'city', 'state', 'pincode', 'is_default']
    list_filter = ['address_type', 'city', 'state', 'is_default']
    search_fields = ['user__username', 'user__email', 'address_line_1', 'city']
    ordering = ['-created_at']


@admin.register(OTPVerification)
class OTPVerificationAdmin(admin.ModelAdmin):
    """OTP Verification admin"""
    list_display = ['user', 'verification_type', 'otp_code', 'is_verified', 'expires_at', 'created_at']
    list_filter = ['verification_type', 'is_verified']
    search_fields = ['user__username', 'user__email', 'user__phone']
    ordering = ['-created_at']
    readonly_fields = ['otp_code']


@admin.register(UserWallet)
class UserWalletAdmin(admin.ModelAdmin):
    """User Wallet admin"""
    list_display = ['user', 'balance', 'created_at', 'updated_at']
    search_fields = ['user__username', 'user__email']
    ordering = ['-updated_at']
    readonly_fields = ['balance']


@admin.register(WalletTransaction)
class WalletTransactionAdmin(admin.ModelAdmin):
    """Wallet Transaction admin"""
    list_display = ['wallet', 'transaction_type', 'amount', 'source', 'reference_id', 'created_at']
    list_filter = ['transaction_type', 'source']
    search_fields = ['wallet__user__username', 'reference_id', 'description']
    ordering = ['-created_at']
    readonly_fields = ['created_at']
