from django.urls import path
from . import views

urlpatterns = [
    path('', views.ShopListCreateView.as_view(), name='shop-list-create'),
    path('<uuid:pk>/', views.ShopDetailView.as_view(), name='shop-detail'),
    path('documents/', views.VendorDocumentUploadView.as_view(), name='vendor-documents'),
    path('<uuid:pk>/approve/', views.approve_shop, name='shop-approve'),
    path('<uuid:pk>/reject/', views.reject_shop, name='shop-reject'),
]
