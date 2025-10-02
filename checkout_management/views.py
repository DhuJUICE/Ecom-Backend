from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
import json
import uuid
import hashlib
from urllib.parse import quote_plus, unquote_plus
import requests

# PayFast credentials
PAYFAST_MERCHANT_ID = settings.PAYFAST_TEST_MERCHANT_ID
PAYFAST_MERCHANT_KEY = settings.PAYFAST_TEST_MERCHANT_KEY
PAYFAST_SANDBOX = True  # Set False for production
PAYFAST_URL = (
    "https://sandbox.payfast.co.za/eng/process"
    if PAYFAST_SANDBOX
    else "https://www.payfast.co.za/eng/process"
)

def checkout(request):
    """
    Initiates PayFast payment.
    Expects POST JSON with 'totalPurchaseTotal'.
    """
    if request.method != "POST":
        return JsonResponse({"success": False, "error": "Invalid request method."}, status=405)

    try:
        data = json.loads(request.body)
        amount = float(data.get("totalPurchaseTotal", 0))
        # Generate a unique transaction ID
        m_payment_id = str(uuid.uuid4())

        # Build PayFast payload
        payload = {
            "merchant_id": PAYFAST_MERCHANT_ID,
            "merchant_key": PAYFAST_MERCHANT_KEY,
            "return_url": "https://yourdomain.com/payment-success",
            "cancel_url": "https://yourdomain.com/payment-cancel",
            "notify_url": "https://copyrights-virtue-partnership-obtaining.trycloudflare.com/ipn",
            "m_payment_id": m_payment_id,
            "amount": "%.2f" % amount,
            "item_name": f"Order #{m_payment_id}",
            "name_first": "John",
            "name_last": "Doe",
            "email_address": "john@example.com",
        }

        # Construct PayFast URL
        payment_url = f"{PAYFAST_URL}?{'&'.join(f'{k}={v}' for k,v in payload.items())}"
        return JsonResponse({"success": True, "payment_url": payment_url})

    except Exception as e:
        return JsonResponse({"success": False, "error": str(e)}, status=500)

@csrf_exempt
def payfast_ipn(request):
    if request.method != "POST":
        return HttpResponse("Invalid request method", status=405)

    # Convert POST body to dict
    raw_body = request.body.decode("utf-8")
    data = {k: v for k, v in [pair.split('=') for pair in raw_body.split('&') if '=' in pair]}

    # Validate with PayFast
    response = requests.post(
        "https://sandbox.payfast.co.za/eng/query/validate",  # change to production URL in prod
        data=data
    )

    if response.text == "VALID":
        if data.get("payment_status") == "COMPLETE":
            print("Successful payment")
            return HttpResponse("Payment received", status=200)
        else:
            print("Payment not complete")
            return HttpResponse("Payment not complete", status=400)
    else:
        print("IPN could not be validated by PayFast")
        return HttpResponse("Invalid IPN", status=400)