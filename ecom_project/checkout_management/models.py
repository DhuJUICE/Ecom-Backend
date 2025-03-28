from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class TRANSACTION_LOG(models.Model):
    # Reference to the user who made the transaction
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    
    # Store transaction items with their quantities as a JSON object
    menuCartItems = models.JSONField(
        default=dict,
        help_text="Dictionary where keys are MENU item IDs and values are quantities"
    )
    
    # Track the date and time the transaction was made
    datetimeUpdated = models.DateTimeField(auto_now=True)

    # Payment method: either 'cash' or 'card'
    paymentMethod = models.CharField(
        max_length=10,
        choices=[("cash", "Cash"), ("card", "Card")],
        help_text="Payment method used for the transaction", 
        default="card"  # Default to "card"
    )