from django.urls import path
from . import views

urlpatterns = [
    path('razorpay/create-order/<uuid:order_id>/', views.create_razorpay_order, name='create-razorpay-order'),
    path('razorpay/webhook/', views.razorpay_webhook, name='razorpay-webhook'),
]
