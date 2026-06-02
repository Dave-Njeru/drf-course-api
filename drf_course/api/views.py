from django.db.models import Max
from api.serializers import ProductSerializer, OrderSerializer, ProductInfoSerializer
from api.models import Product, Order
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import generics

class ProductListAPIView(generics.ListAPIView):
    queryset = Product.objects.filter(stock__gt=0)  # Only return products that are in stock
    serializer_class = ProductSerializer

class ProductDetailAPIView(generics.RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class OrderListAPIView(generics.ListAPIView):
    queryset = Order.objects.prefetch_related('items__product')  # Optimize query to fetch related products
    serializer_class = OrderSerializer

# Aggregate API data for products info
@api_view(['GET'])
def products_info(request):
    products = Product.objects.all()
    serializer = ProductInfoSerializer({
        'products': products,
        'count': len(products),
        'max_price': products.aggregate(max_price=Max('price'))['max_price']
    })
    return Response(serializer.data)