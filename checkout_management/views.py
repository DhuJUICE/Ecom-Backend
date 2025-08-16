from django.shortcuts import render
from django.http import JsonResponse
from rest_framework.views import APIView
from .models import TRANSACTION_LOG
from cart_management.models import CART
from api_management.serializers import TransactionSerializer
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
import json
import requests

PAYSTACK_SECRET_KEY = settings.PAYSTACK_SECRET_KEY
@csrf_exempt
def checkout(request):
    """
    Handles Paystack payment verification.
    Expects POST JSON with 'totalPurchaseTotal' and 'reference'.
    """
    if request.method != 'POST':
        return JsonResponse({"success": False, "error": "Invalid request method."}, status=405)

    try:
        data = json.loads(request.body)
        amount_in_rands = int(float(data.get('totalPurchaseTotal', 0)))
        reference = data.get('reference')  # Paystack payment reference

        if not reference:
            return JsonResponse({"success": False, "error": "Missing payment reference."}, status=400)

        # Verify payment with Paystack
        headers = {"Authorization": f"Bearer {settings.PAYSTACK_SECRET_KEY}"}
        verify_url = f"https://api.paystack.co/transaction/verify/{reference}"
        response = requests.get(verify_url, headers=headers)
        result = response.json()

        if result['status'] and result['data']['status'] == 'success':
            # Payment successful
            success_message = f"Your payment of R{amount_in_rands} was successfully processed."
            return JsonResponse({"success": True, "message": success_message}, status=200)
        else:
            fail_message = f"Payment verification failed. Try again later."
            return JsonResponse({"success": False, "message": fail_message}, status=400)

    except Exception as e:
        return JsonResponse({"success": False, "error": str(e)}, status=500)