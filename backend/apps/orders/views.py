from rest_framework import generics, permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from .models import Order
from .serializers import OrderSerializer


class OrderListCreateView(generics.ListCreateAPIView):
    serializer_class = OrderSerializer

    def get_permissions(self):
        if self.request.method == 'POST':
            return [permissions.IsAuthenticated()]
        return [permissions.IsAuthenticated()]

    def get_queryset(self):
        user = self.request.user
        if user.role == 'customer':
            return Order.objects.filter(customer=user)
        if user.role == 'vendor':
            return Order.objects.filter(items__product__shop__vendor=user).distinct()
        if user.role == 'delivery_partner':
            return Order.objects.filter(delivery_partner=user)
        return Order.objects.all()


class OrderDetailView(generics.RetrieveUpdateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]


@api_view(['POST'])
@permission_classes([permissions.IsAdminUser])
def assign_order(request, pk):
    delivery_partner_id = request.data.get('delivery_partner_id')
    try:
        order = Order.objects.get(pk=pk)
        order.delivery_partner_id = delivery_partner_id
        order.status = 'assigned'
        order.save()
        return Response({'message': 'Order assigned'})
    except Order.DoesNotExist:
        return Response({'error': 'Order not found'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def update_delivery_status(request, pk):
    status_value = request.data.get('status')
    try:
        order = Order.objects.get(pk=pk, delivery_partner=request.user)
        order.status = status_value
        order.save()
        return Response({'message': 'Status updated'})
    except Order.DoesNotExist:
        return Response({'error': 'Order not found'}, status=status.HTTP_404_NOT_FOUND)
