from rest_framework import generics, status, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.contrib.auth import login, logout
from django.utils import timezone
from datetime import timedelta
import random
import string

from .models import User, UserAddress, OTPVerification, UserWallet, WalletTransaction
from .serializers import (
    UserRegistrationSerializer, UserLoginSerializer, UserProfileSerializer,
    UserAddressSerializer, OTPVerificationSerializer, OTPRequestSerializer,
    UserWalletSerializer, WalletTransactionSerializer, PasswordChangeSerializer,
    PasswordResetSerializer, PasswordResetConfirmSerializer
)
from .utils import send_otp_sms, send_otp_email


class UserRegistrationView(generics.CreateAPIView):
    """User registration endpoint"""
    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer
    permission_classes = [permissions.AllowAny]
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        
        # Generate and send OTP for phone verification
        self.send_verification_otp(user, 'phone')
        
        return Response({
            'message': 'User registered successfully. Please verify your phone number.',
            'user_id': user.id
        }, status=status.HTTP_201_CREATED)
    
    def send_verification_otp(self, user, verification_type):
        """Generate and send OTP for verification"""
        otp_code = ''.join(random.choices(string.digits, k=6))
        expires_at = timezone.now() + timedelta(minutes=10)
        
        OTPVerification.objects.create(
            user=user,
            verification_type=verification_type,
            otp_code=otp_code,
            expires_at=expires_at
        )
        
        if verification_type == 'phone':
            send_otp_sms(user.phone, otp_code)
        elif verification_type == 'email':
            send_otp_email(user.email, otp_code)


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def login_view(request):
    """User login endpoint"""
    serializer = UserLoginSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.validated_data['user']
        login(request, user)
        
        # Create or get token
        token, created = Token.objects.get_or_create(user=user)
        
        return Response({
            'token': token.key,
            'user': UserProfileSerializer(user).data,
            'message': 'Login successful'
        })
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def logout_view(request):
    """User logout endpoint"""
    try:
        # Delete the user's token
        Token.objects.filter(user=request.user).delete()
        logout(request)
        return Response({'message': 'Logout successful'})
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


class UserProfileView(generics.RetrieveUpdateAPIView):
    """User profile endpoint"""
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_object(self):
        return self.request.user


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def request_otp(request):
    """Request OTP for verification"""
    serializer = OTPRequestSerializer(data=request.data)
    if serializer.is_valid():
        verification_type = serializer.validated_data['verification_type']
        user = request.user
        
        # Generate OTP
        otp_code = ''.join(random.choices(string.digits, k=6))
        expires_at = timezone.now() + timedelta(minutes=10)
        
        # Delete existing OTPs
        OTPVerification.objects.filter(
            user=user,
            verification_type=verification_type,
            is_verified=False
        ).delete()
        
        # Create new OTP
        OTPVerification.objects.create(
            user=user,
            verification_type=verification_type,
            otp_code=otp_code,
            expires_at=expires_at
        )
        
        # Send OTP
        if verification_type == 'phone':
            send_otp_sms(user.phone, otp_code)
        elif verification_type == 'email':
            send_otp_email(user.email, otp_code)
        
        return Response({'message': f'OTP sent to your {verification_type}'})
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def verify_otp(request):
    """Verify OTP"""
    serializer = OTPVerificationSerializer(data=request.data)
    if serializer.is_valid():
        verification_type = serializer.validated_data['verification_type']
        otp_code = serializer.validated_data['otp_code']
        user = request.user
        
        try:
            otp = OTPVerification.objects.get(
                user=user,
                verification_type=verification_type,
                otp_code=otp_code,
                is_verified=False,
                expires_at__gt=timezone.now()
            )
            
            # Mark OTP as verified
            otp.is_verified = True
            otp.save()
            
            # Update user verification status
            if verification_type == 'phone':
                user.is_phone_verified = True
            elif verification_type == 'email':
                user.is_email_verified = True
            
            # Update user status if both phone and email are verified
            if user.is_phone_verified and user.is_email_verified:
                user.status = 'active'
            
            user.save()
            
            return Response({'message': f'{verification_type.title()} verified successfully'})
            
        except OTPVerification.DoesNotExist:
            return Response({'error': 'Invalid or expired OTP'}, status=status.HTTP_400_BAD_REQUEST)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserAddressListCreateView(generics.ListCreateAPIView):
    """User addresses list and create endpoint"""
    serializer_class = UserAddressSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return UserAddress.objects.filter(user=self.request.user)


class UserAddressDetailView(generics.RetrieveUpdateDestroyAPIView):
    """User address detail endpoint"""
    serializer_class = UserAddressSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return UserAddress.objects.filter(user=self.request.user)


class UserWalletView(generics.RetrieveAPIView):
    """User wallet endpoint"""
    serializer_class = UserWalletSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_object(self):
        wallet, created = UserWallet.objects.get_or_create(user=self.request.user)
        return wallet


class WalletTransactionListView(generics.ListAPIView):
    """Wallet transactions list endpoint"""
    serializer_class = WalletTransactionSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        wallet = UserWallet.objects.get(user=self.request.user)
        return WalletTransaction.objects.filter(wallet=wallet)


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def change_password(request):
    """Change password endpoint"""
    serializer = PasswordChangeSerializer(data=request.data, context={'request': request})
    if serializer.is_valid():
        user = request.user
        user.set_password(serializer.validated_data['new_password'])
        user.save()
        
        # Delete all tokens to force re-login
        Token.objects.filter(user=user).delete()
        
        return Response({'message': 'Password changed successfully. Please login again.'})
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def password_reset_request(request):
    """Password reset request endpoint"""
    serializer = PasswordResetSerializer(data=request.data)
    if serializer.is_valid():
        email = serializer.validated_data['email']
        try:
            user = User.objects.get(email=email)
            # Generate reset token (implement token generation logic)
            # Send reset email (implement email sending logic)
            return Response({'message': 'Password reset email sent'})
        except User.DoesNotExist:
            return Response({'message': 'Password reset email sent'})  # Don't reveal if email exists
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def password_reset_confirm(request):
    """Password reset confirmation endpoint"""
    serializer = PasswordResetConfirmSerializer(data=request.data)
    if serializer.is_valid():
        # Implement token validation and password reset logic
        return Response({'message': 'Password reset successful'})
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
