from api.serializers import ProductSerializer
from api.models import Product
from django.http import JsonResponse
# from rest_framework.response import Response
# from rest_framework.renderers import JSONRenderer

def product_list(request):
    products = Product.objects.all()
    serializer = ProductSerializer(products, many=True)
    return JsonResponse({
        'data': serializer.data
    })
