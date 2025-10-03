from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt

from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import status
from rest_framework.response import Response

import json

# Models
from product_management.models import PRODUCT
from cart_management.models import CART
from django.contrib.auth.models import User

# Serializers
from .serializers import *

# Utility / Other views
from checkout_management.views import checkout
from user_management.views import *
from product_management.views import ProductManagement as PMView
from checkout_management.views import *

# Import the cart endpoint classes from cart_management
from cart_management.views import (
    AddToCart as AddToCartView,
    CartManagement as CartManagementView,
    CartRemoveProduct as CartRemoveProductView,
    CartIncrementProduct as CartIncrementProductView,
    CartDecrementProduct as CartDecrementProductView,
	CartMainManagement as CartMainView
)

# Date/time utility
from django.utils.timezone import now as timezone_now

#-------------------------------------------------------------
# Basic page view
def DisplayPage(request):
    return render(request, 'api_template.html')

#-------------------------------------------------------------
# API Endpoint for Signup/Register
class Register(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        response = register_view(request)
        if isinstance(response, JsonResponse):
            return JsonResponse(json.loads(response.content), status=response.status_code)
        return JsonResponse({"error": "Unexpected response type"}, status=500)


#-------------------------------------------------------------
class ProductManagement(APIView):
    permission_classes = [AllowAny]

    def get(self, request, pk=None):
        """
        Delegates GET request to the ProductManagement view in product_management app.
        """
        view = PMView()
        response = view.get(request, pk=pk)
        if hasattr(response, "data"):
            return JsonResponse(response.data, status=response.status_code, safe=False)
        return JsonResponse({"error": "Unexpected response type"}, status=500)

    def post(self, request):
        """
        Delegates POST request (if needed) to ProductManagement view.
        """
        view = PMView()
        response = view.post(request)
        if hasattr(response, "data"):
            return JsonResponse(response.data, status=response.status_code, safe=False)
        return JsonResponse({"error": "Unexpected response type"}, status=500)

    def put(self, request, pk=None):
        """
        Delegates PUT request to ProductManagement view.
        """
        view = PMView()
        response = view.put(request, pk=pk)
        if hasattr(response, "data"):
            return JsonResponse(response.data, status=response.status_code, safe=False)
        return JsonResponse({"error": "Unexpected response type"}, status=500)

    def delete(self, request, pk=None):
        """
        Delegates DELETE request to ProductManagement view.
        """
        view = PMView()
        response = view.delete(request, pk=pk)
        if hasattr(response, "data"):
            return JsonResponse(response.data, status=response.status_code, safe=False)
        return JsonResponse({"error": "Unexpected response type"}, status=500)

#-------------------------------------------------------------
# CART MANAGEMENT API ENDPOINTS (using imported views)

class AddToCart(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        return AddToCartView().post(request)


class CartManagement(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return CartManagementView().get(request)

    def post(self, request):
        return CartManagementView().post(request)

    def put(self, request, cart_id):
        return CartManagementView().put(request, cart_id)

    def delete(self, request, cart_id):
        return CartManagementView().delete(request, cart_id)


class CartRemoveProduct(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request):
        return CartRemoveProductView().put(request)


class CartIncrementProduct(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request):
        return CartIncrementProductView().put(request)


class CartDecrementProduct(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request):
        return CartDecrementProductView().put(request)

#=============================
# Single cart endpoint through API
class CartMainManagement(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # Delegate GET request to the cart_management view
        return CartMainView().get(request)

    def put(self, request):
        # Delegate PUT request (all actions: add/remove/inc/dec)
        return CartMainView().put(request)
#-------------------------------------------------------------
# CHECKOUT MANAGEMENT API ENDPOINTS
class CheckoutManagement(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        return checkout(request)
