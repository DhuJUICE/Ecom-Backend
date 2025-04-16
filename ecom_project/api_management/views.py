from django.shortcuts import render

#permissions for authentication and security
from rest_framework.permissions import AllowAny
from rest_framework.permissions import IsAuthenticated

from rest_framework.views import APIView
from django.http import JsonResponse
from rest_framework import status
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
import json

#Model Imports
from product_management.models import PRODUCT
from cart_management.models import CART
from browse_management.models import MENU
from django.contrib.auth.models import User
from checkout_management.models import TRANSACTION_LOG

#Serializers imports
from .serializers import *

#User management functionality imports
from user_management.views import *

#User management functionality imports
from checkout_management.views import *

#date usage imports
from django.utils.timezone import now as timezone_now

# Create your views here.
def DisplayPage(request):
    return render(request, 'api_template.html')
#
########
#IMAGEKIT ENDPOINT TO CREATE AND RETURN TOKEN FOR AUTHENTICATION
import hashlib
import hmac
import time
from django.http import JsonResponse
from django.conf import settings  # Ensure the ImageKit private key is set in settings

def generate_imagekit_auth(request):
    # Random unique token
    token = str(uuid.uuid4())

    # Expiry timestamp (e.g., 1 minute from now)
    expire = int(time.time()) + 60

    # String to sign: token + expire
    string_to_sign = token + str(expire)

    # Generate signature using private key
    signature = hmac.new(
        key=settings.IMAGEKIT_PRIVATE_KEY.encode(),
        msg=string_to_sign.encode(),
        digestmod=hashlib.sha1
    ).hexdigest()

    return JsonResponse({
        'token': token,
        'expire': expire,
        'signature': signature
    })

#___________________________________________________________
#USER MANAGEMENT API ENDPOINTS
#API ENDPOINT FOR LOGIN
class Login(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        # Call the regular function
        response = login_view(request)

        # If the other function returns a JsonResponse, return its content as JSON
        if isinstance(response, JsonResponse):
            # Deserialize the content if it's a JsonResponse
            return JsonResponse(json.loads(response.content), status=response.status_code)

        # Handle other response types if necessary
        return JsonResponse({"error": "Unexpected response type"}, status=500)

#API ENDPOINT FOR SIGNUP/REGISTER
class Register(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        # Call the regular function
        response = register_view(request)

        # If the other function returns a JsonResponse, return its content as JSON
        if isinstance(response, JsonResponse):
            # Deserialize the content if it's a JsonResponse
            return JsonResponse(json.loads(response.content), status=response.status_code)

        # Handle other response types if necessary
        return JsonResponse({"error": "Unexpected response type"}, status=500)

#API ENDPOINT FOR LOGOUT
class Logout(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        # Call the regular function
        response = logout_view(request)

        # If the other function returns a JsonResponse, return its content as JSON
        if isinstance(response, JsonResponse):
            # Deserialize the content if it's a JsonResponse
            return JsonResponse(json.loads(response.content), status=response.status_code)

        # Handle other response types if necessary
        return JsonResponse({"error": "Unexpected response type"}, status=500)
#___________________________________________________________
#PRODUCT MANAGEMENT API ENDPOINTS
class ProductManagement(APIView):
    permission_classes = [AllowAny]

    # Get all products or a specific product by ID
    def get(self, request, pk=None):
        if pk:
            try:
                product = PRODUCT.objects.get(pk=pk)
                serializer = ProductSerializer(product)
                return Response(serializer.data, status=status.HTTP_200_OK)
            except PRODUCT.DoesNotExist:
                return Response({"error": "Product not found"}, status=status.HTTP_404_NOT_FOUND)
        else:
            products = PRODUCT.objects.all()
            serializer = ProductSerializer(products, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

    # Add a new product
    def post(self, request):
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # Update an existing product
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

    # Delete a product
    def delete(self, request, pk):
        try:
            product = PRODUCT.objects.get(pk=pk)
            product.delete()
            return Response({"message": "Product deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
        except PRODUCT.DoesNotExist:
            return Response({"error": "Product not found"}, status=status.HTTP_404_NOT_FOUND)
#___________________________________________________________
class AddToCart(APIView):
    permission_classes = [IsAuthenticated]

    """
    API endpoint for managing ADDING to the CART model.
    Supports POST
    """

    def post(self, request):
        """
        Add or update a menu item in the user's cart.
        """
        try:
            user = request.user  # Get the authenticated user
            data = request.data
            product_id = str(data.get("productId"))  # Convert to string for dictionary key
            quantity = int(data.get("quantity", 1))  # Default quantity is 1

            if not product_id:
                return JsonResponse({"success": False, "error": "Product ID is required"}, status=400)

            # Get or create the cart for the user
            cart, created = CART.objects.get_or_create(user=user)

            # Load existing menuCartItems
            cart_items = cart.menuCartItems

            # Update quantity if item already exists, otherwise add new item
            if product_id in cart_items:
                cart_items[product_id] = quantity
            else:
                cart_items[product_id] = quantity

            # Save the updated cart
            cart.menuCartItems = cart_items
            cart.save()

            return JsonResponse({"success": True, "cart": cart_items}, status=200)

        except Exception as e:
            return JsonResponse({"success": False, "error": str(e)}, status=500)

#CART MANAGEMENT API ENDPOINTS
class CartManagement(APIView):
    permission_classes = [IsAuthenticated]

    """
    API endpoint for managing the CART model.
    Supports GET, POST, PUT, DELETE.
    """
    def get(self, request):
        try:
            # Check if the user is authenticated
            if not request.user.is_authenticated:
                return JsonResponse({"success": False, "message": "Please log in to see your cart."}, status=401)
            
            # Get the cart for the authenticated user
            cart = CART.objects.get(user=request.user.id)

            user_id = request.user.id

            # Extract menuCartItems
            cart_items = cart.menuCartItems  # This is already stored as a dictionary
            print(str(cart_items))
            return JsonResponse({"success": True, "cart": cart_items, "user_id":user_id}, status=200)

        except CART.DoesNotExist:
            return JsonResponse({"success": False, "cart": {}}, status=200)  # Return empty cart if not found
        except Exception as e:
            return JsonResponse({"success": False, "error": str(e)}, status=500)

    def post(self, request):
        """
        Create a new cart item.
        Returns JSON response.
        """
        try:
            serializer = CartSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return JsonResponse({"success": True, "data": serializer.data}, status=201)
            return JsonResponse({"success": False, "errors": serializer.errors}, status=400)
        except Exception as e:
            return JsonResponse({"success": False, "error": str(e)}, status=500)

    def put(self, request, cart_id):
        """
        Update an existing cart item.
        Returns JSON response.
        """
        try:
            cart_item = CART.objects.get(id=cart_id)
            serializer = CartSerializer(cart_item, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return JsonResponse({"success": True, "data": serializer.data}, status=200)
            return JsonResponse({"success": False, "errors": serializer.errors}, status=400)
        except CART.DoesNotExist:
            return JsonResponse({"success": False, "error": "Cart item not found"}, status=404)
        except Exception as e:
            return JsonResponse({"success": False, "error": str(e)}, status=500)

    def delete(self, request, cart_id):
        """
        Delete a cart item.
        Returns JSON response.
        """
        try:
            cart_item = CART.objects.get(id=cart_id)
            cart_item.delete()
            return JsonResponse({"success": True, "message": "Cart item deleted successfully"}, status=204)
        except CART.DoesNotExist:
            return JsonResponse({"success": False, "error": "Cart item not found"}, status=404)
        except Exception as e:
            return JsonResponse({"success": False, "error": str(e)}, status=500)

class CartRemoveProduct(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request):
        """
        Remove a menu item from the user's cart.
        """
        try:
            user = request.user
            data = request.data
            product_id = str(data.get("productId"))

            if not product_id:
                return JsonResponse({"success": False, "error": "Product ID is required"}, status=400)

            # Get the user's cart
            cart = CART.objects.filter(user=user).first()
            if not cart:
                return JsonResponse({"success": False, "error": "Cart not found"}, status=404)

            # Load existing menuCartItems
            cart_items = cart.menuCartItems or {}

            # Remove the product if it exists
            if product_id in cart_items:
                del cart_items[product_id]
                cart.menuCartItems = cart_items
                cart.save()
                return JsonResponse({"success": True, "message": "Product removed from cart", "cart": cart_items}, status=200)
            else:
                return JsonResponse({"success": False, "error": "Product is not in user's cart"}, status=400)

        except Exception as e:
            return JsonResponse({"success": False, "error": str(e)}, status=500)

#api view functionality to increment a certain products quantity by 1 
class CartIncrementProduct(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request):
        """
        Increment a menu item quantity in the user's cart.
        """
        try:
            user = request.user
            data = request.data
            product_id = str(data.get("productId"))

            if not product_id:
                return JsonResponse({"success": False, "error": "Product ID is required"}, status=400)

            # Get the user's cart
            cart = CART.objects.filter(user=user).first()
            if not cart:
                return JsonResponse({"success": False, "error": "Cart not found"}, status=404)

            # Ensure cart_items is always a dictionary
            cart_items = cart.menuCartItems or {}

            # Increment the quantity if the product exists
            if product_id in cart_items:
                cart_items[product_id] += 1  # Increment quantity
            else:
                return JsonResponse({"success": False, "error": "Product is not in user's cart"}, status=400)

            # Save the updated cart
            cart.menuCartItems = cart_items
            cart.save()

            return JsonResponse({"success": True, "message": "Product quantity incremented in user's cart", "cart": cart_items}, status=200)

        except Exception as e:
            return JsonResponse({"success": False, "error": str(e)}, status=500)

#api view functionality to decrement a certain products quantity by 1 
class CartDecrementProduct(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request):
        """
        Decrement a menu item quantity in the user's cart.
        """
        try:
            user = request.user
            data = request.data
            product_id = str(data.get("productId"))

            if not product_id:
                return JsonResponse({"success": False, "error": "Product ID is required"}, status=400)

            # Get the user's cart
            cart = CART.objects.filter(user=user).first()
            if not cart:
                return JsonResponse({"success": False, "error": "Cart not found"}, status=404)

            # Ensure cart_items is always a dictionary
            cart_items = cart.menuCartItems or {}

            # Check if the product exists in the cart
            if product_id in cart_items:
                if cart_items[product_id] > 1:
                    cart_items[product_id] -= 1  # Decrement quantity
                else:
                    return JsonResponse({"success": False, "error": "Cannot decrement further, quantity is already 1"}, status=400)
            else:
                return JsonResponse({"success": False, "error": "Product is not in user's cart"}, status=400)

            # Save the updated cart
            cart.menuCartItems = cart_items
            cart.save()

            return JsonResponse({"success": True, "message": "Product quantity decremented in user's cart", "cart": cart_items}, status=200)

        except Exception as e:
            return JsonResponse({"success": False, "error": str(e)}, status=500)

#___________________________________________________________
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

#TRANSACTION MANAGEMENT API ENDPOINTS
class TransactionManagement(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, transaction_id=None):
        if transaction_id:
            try:
                transaction = TRANSACTION_LOG.objects.get(id=transaction_id)
                serializer = TransactionSerializer(transaction)
                return JsonResponse({"success": True, "data": serializer.data}, status=200)
            except TRANSACTION_LOG.DoesNotExist:
                return JsonResponse({"success": False, "error": "Transaction not found"}, status=404)

        transactions = TRANSACTION_LOG.objects.all()
        serializer = TransactionSerializer(transactions, many=True)
        return JsonResponse({"success": True, "data": serializer.data}, status=200, safe=False)

    def post(self, request):
        try:
            user = request.user  # Get the authenticated user

            # Get the user's cart
            cart = get_object_or_404(CART, user=user)

            # Get the payment method from request data
            payment_method = request.data.get("paymentMethod")
            
            if payment_method not in ["cash", "card"]:
                return JsonResponse({"error": "Invalid payment method. Choose 'cash' or 'card'."}, status=400)

            # Check if the cart is empty
            if not cart.menuCartItems:
                return JsonResponse({"error": "Cart is empty, cannot process transaction."}, status=400)

            # Create a transaction log entry
            transaction = TRANSACTION_LOG.objects.create(
                user=user,
                menuCartItems=cart.menuCartItems,  # Copy cart items
                paymentMethod=payment_method  # Assign payment method
            )

            # Clear the user's cart
            cart.menuCartItems = {}  # Empty the cart
            cart.save()

            return JsonResponse({"message": "Transaction successful!", "transaction_id": transaction.id}, status=201)

        except CART.DoesNotExist:
            return JsonResponse({"error": "Cart not found for this user."}, status=404)
        except Exception as e:
            print(str(e))
            return JsonResponse({"error": f"An unexpected error occurred: {str(e)}"}, status=500)

    def put(self, request, transaction_id):
        try:
            transaction = TRANSACTION_LOG.objects.get(id=transaction_id)
        except TRANSACTION_LOG.DoesNotExist:
            return JsonResponse({"success": False, "error": "Transaction not found"}, status=404)

        serializer = TransactionSerializer(transaction, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse({"success": True, "data": serializer.data}, status=200)
        return JsonResponse({"success": False, "errors": serializer.errors}, status=400)

    def delete(self, request, transaction_id):
        try:
            transaction = TRANSACTION_LOG.objects.get(id=transaction_id)
        except TRANSACTION_LOG.DoesNotExist:
            return JsonResponse({"success": False, "error": "Transaction not found"}, status=404)

        transaction.delete()
        return JsonResponse({"success": True, "message": "Transaction deleted successfully"}, status=204)
#___________________________________________________________


import stripe
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json


#CHECKOUT MANAGEMENT API ENDPOINTS
stripe.api_key = settings.STRIPE_TEST_SECRET_KEY

class CheckoutManagement(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        stripe_token = request.POST.get('stripeToken')
        total_price = int(float(request.POST.get('totalPurchaseTotal'))) * 100 # Amount in cents

        try:
            # Create a charge (you can also use a PaymentIntent depending on your use case)
            charge = stripe.Charge.create(
                amount=total_price,
                currency='zar',  # You can change this to your currency (e.g., 'zar' for South African Rand)
                source=stripe_token,
                description='Payment for your order',
            )
            return JsonResponse({'status': 'success', 'charge': charge})
        except stripe.error.StripeError as e:
            return JsonResponse({'status': 'error', 'message': str(e)})