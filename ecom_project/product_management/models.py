from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class PRODUCT(models.Model):

    #product details for database
    prodName = models.CharField(max_length = 100)
    prodPrice = models.DecimalField(max_digits=10, decimal_places=2)
    prodDesc = models.CharField(max_length = 100)
    prodAvailQuant = models.IntegerField()
    prodOnMenu =  models.BooleanField(default=False)
    prodImagePath = models.CharField(max_length=255, blank=True, null=True)
    uploadUser = models.ForeignKey(
        User,               # The related model
        on_delete=models.CASCADE,  # What happens when the related user is deleted
        related_name='uploads',    # Optional: reverse relation name
        null=False,                # Is this field required? Default is False
        blank=False                # Required in forms
    )
    moderation_status = models.CharField(
    max_length=10,
    choices=[('pending', 'Pending'), ('approved', 'Approved'), ('rejected', 'Rejected')],
    default='pending'
)