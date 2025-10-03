from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

# Models
from .models import CART

# Serializers
from api_management.serializers import *

#+++++===============================
class CartManagement(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request):
        """
        Handles all cart operations: add, remove, increment, decrement.
        Request body should contain:
        {
            "action": "add|remove|increment|decrement",
            "productId": "<id>",
            "quantity": <optional, for add>
            "prodName": "<name>",       # required for add
            "prodPrice": "<price>",     # required for add
            "prodImagePath": "<image>"  # required for add
        }
        """
        try:
            user = request.user
            data = request.data
            action = data.get("action")
            product_id = str(data.get("productId"))

            if not action or not product_id:
                return JsonResponse({"success": False, "error": "Action and productId are required"}, status=400)

            cart, _ = CART.objects.get_or_create(user=user)
            cart_items = cart.menuCartItems or {}

            if action == "add":
                quantity = int(data.get("quantity", 1))
                prod_name = data.get("prodName")
                prod_price = data.get("prodPrice")
                prod_image = data.get("prodImagePath")

                if not all([prod_name, prod_price, prod_image]):
                    return JsonResponse({"success": False, "error": "Product name, price, and image are required for adding"}, status=400)

                cart_items[product_id] = {
                    "id": product_id,
                    "prodName": prod_name,
                    "prodPrice": prod_price,
                    "prodImagePath": prod_image,
                    "quantity": quantity
                }

            elif action == "remove":
                if product_id in cart_items:
                    del cart_items[product_id]
                else:
                    return JsonResponse({"success": False, "error": "Product not in cart"}, status=400)

            elif action == "increment":
                if product_id in cart_items:
                    cart_items[product_id]["quantity"] += 1
                else:
                    return JsonResponse({"success": False, "error": "Product not in cart"}, status=400)

            elif action == "decrement":
                if product_id in cart_items:
                    if cart_items[product_id]["quantity"] > 1:
                        cart_items[product_id]["quantity"] -= 1
                    else:
                        return JsonResponse({"success": False, "error": "Quantity already 1, cannot decrement further"}, status=400)
                else:
                    return JsonResponse({"success": False, "error": "Product not in cart"}, status=400)
            else:
                return JsonResponse({"success": False, "error": "Invalid action"}, status=400)

            cart.menuCartItems = cart_items
            cart.save()

            return JsonResponse({"success": True, "cart": cart_items}, status=200)

        except Exception as e:
            return JsonResponse({"success": False, "error": str(e)}, status=500)

    def get(self, request):
        """
        Returns the current cart for the logged-in user.
        """
        try:
            cart = CART.objects.get(user=request.user)
            return JsonResponse({"success": True, "cart": cart.menuCartItems}, status=200)
        except CART.DoesNotExist:
            return JsonResponse({"success": True, "cart": {}}, status=200)
        except Exception as e:
            return JsonResponse({"success": False, "error": str(e)}, status=500)