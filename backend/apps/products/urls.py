from django.urls import path
from . import views

urlpatterns = [
    path('categories/', views.CategoryListView.as_view(), name='category-list'),
    path('', views.ProductListCreateView.as_view(), name='product-list-create'),
    path('<uuid:pk>/', views.ProductDetailView.as_view(), name='product-detail'),
]
