from django.urls import path
from . import views

urlpatterns = [
    # Authentication
    path('register/', views.UserRegistrationView.as_view(), name='user-register'),
    path('login/', views.login_view, name='user-login'),
    path('logout/', views.logout_view, name='user-logout'),
    
    # Profile
    path('profile/', views.UserProfileView.as_view(), name='user-profile'),
    
    # OTP Verification
    path('request-otp/', views.request_otp, name='request-otp'),
    path('verify-otp/', views.verify_otp, name='verify-otp'),
    
    # Addresses
    path('addresses/', views.UserAddressListCreateView.as_view(), name='user-addresses'),
    path('addresses/<uuid:pk>/', views.UserAddressDetailView.as_view(), name='user-address-detail'),
    
    # Wallet
    path('wallet/', views.UserWalletView.as_view(), name='user-wallet'),
    path('wallet/transactions/', views.WalletTransactionListView.as_view(), name='wallet-transactions'),
    
    # Password Management
    path('change-password/', views.change_password, name='change-password'),
    path('password-reset/', views.password_reset_request, name='password-reset'),
    path('password-reset-confirm/', views.password_reset_confirm, name='password-reset-confirm'),
]
