from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    USER_ROLES_CHOICES = [
        ('openUser', 'Open Access'),
        ('adminUser', 'Admin'),
        ('moderatorUser', 'Moderator'),
        ('businessOwner', 'Business Owner'),
    ]

    role = models.CharField(max_length=20, choices=USER_ROLES_CHOICES, default='openUser')
    
    # Optional: track if business owner request is pending admin approval
    business_owner_request = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username} - {self.role}"
