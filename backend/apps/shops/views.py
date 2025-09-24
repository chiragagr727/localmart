from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from .models import Shop, VendorDocument
from .serializers import ShopSerializer, VendorDocumentSerializer


class ShopListCreateView(generics.ListCreateAPIView):
    serializer_class = ShopSerializer

    def get_permissions(self):
        if self.request.method == 'POST':
            return [permissions.IsAuthenticated()]
        return [permissions.AllowAny()]

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated and user.role == 'vendor':
            return Shop.objects.filter(vendor=user)
        return Shop.objects.filter(status='approved', is_active=True)


class ShopDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ShopSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Shop.objects.filter(vendor=self.request.user)


class VendorDocumentUploadView(generics.ListCreateAPIView):
    serializer_class = VendorDocumentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return VendorDocument.objects.filter(vendor=self.request.user)

    def perform_create(self, serializer):
        serializer.save(vendor=self.request.user)


@api_view(['POST'])
@permission_classes([permissions.IsAdminUser])
def approve_shop(request, pk):
    try:
        shop = Shop.objects.get(pk=pk)
        shop.status = 'approved'
        shop.is_active = True
        shop.save()
        return Response({'message': 'Shop approved'})
    except Shop.DoesNotExist:
        return Response({'error': 'Shop not found'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['POST'])
@permission_classes([permissions.IsAdminUser])
def reject_shop(request, pk):
    try:
        shop = Shop.objects.get(pk=pk)
        shop.status = 'rejected'
        shop.is_active = False
        shop.save()
        return Response({'message': 'Shop rejected'})
    except Shop.DoesNotExist:
        return Response({'error': 'Shop not found'}, status=status.HTTP_404_NOT_FOUND)
