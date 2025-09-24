from django.urls import path
from . import views

urlpatterns = [
    path('', views.OrderListCreateView.as_view(), name='order-list-create'),
    path('<uuid:pk>/', views.OrderDetailView.as_view(), name='order-detail'),
    path('<uuid:pk>/assign/', views.assign_order, name='order-assign'),
    path('<uuid:pk>/delivery-status/', views.update_delivery_status, name='delivery-status'),
]
