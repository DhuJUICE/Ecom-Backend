from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework import status
from rest_framework.response import Response

# Models
from .models import PRODUCT

# Serializers
from api_management.serializers import ProductSerializer


# PRODUCT MANAGEMENT API ENDPOINTS
class ProductManagement(APIView):
    permission_classes = [AllowAny]

    def get(self, request, pk=None):
        if pk:
            try:
                product = PRODUCT.objects.get(pk=pk)
                serializer = ProductSerializer(product)
                return Response(serializer.data, status=status.HTTP_200_OK)
            except PRODUCT.DoesNotExist:
                return Response({"error": "Product not found"}, status=status.HTTP_404_NOT_FOUND)
        else:
            products = PRODUCT.objects.filter(moderation_status="approved")
            serializer = ProductSerializer(products, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        try:
            product = PRODUCT.objects.get(pk=pk)
        except PRODUCT.DoesNotExist:
            return Response({"error": "Product not found"}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = ProductSerializer(product, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        try:
            product = PRODUCT.objects.get(pk=pk)
            product.delete()
            return Response({"message": "Product deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
        except PRODUCT.DoesNotExist:
            return Response({"error": "Product not found"}, status=status.HTTP_404_NOT_FOUND)
