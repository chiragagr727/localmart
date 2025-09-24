from rest_framework import generics, permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.conf import settings
import razorpay
from .models import Payment
from .serializers import PaymentSerializer
from apps.orders.models import Order


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def create_razorpay_order(request, order_id):
    try:
        order = Order.objects.get(pk=order_id, customer=request.user)
    except Order.DoesNotExist:
        return Response({'error': 'Order not found'}, status=status.HTTP_404_NOT_FOUND)

    client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
    data = {"amount": int(order.total * 100), "currency": "INR"}
    rp_order = client.order.create(data=data)

    payment, _ = Payment.objects.get_or_create(order=order, defaults={
        'amount': order.total,
        'currency': 'INR',
        'status': 'created',
        'provider': 'razorpay',
        'provider_order_id': rp_order.get('id')
    })

    return Response({
        'razorpay_order_id': rp_order.get('id'),
        'amount': data['amount'],
        'currency': 'INR',
        'key': settings.RAZORPAY_KEY_ID
    })


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def razorpay_webhook(request):
    # Placeholder to handle Razorpay webhooks (payment authorized, captured, failed)
    # Verify signature and update Payment + Order statuses accordingly.
    return Response({'status': 'received'})
