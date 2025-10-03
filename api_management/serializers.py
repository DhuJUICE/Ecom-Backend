from rest_framework import serializers
from product_management.models import PRODUCT
from cart_management.models import CART
from django.contrib.auth.models import User

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from user_management.models import UserProfile

#custom serializer to add a field to the returned data from token endpoint
class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)

        # Add custom fields to the response data
        data['is_staff'] = self.user.is_staff
        data['user_id'] = self.user.id
        return data

class ProductSerializer(serializers.ModelSerializer):
    uploadUser = serializers.PrimaryKeyRelatedField(read_only=True)  # Prevent trying to update it
    prodImagePath = serializers.CharField(required=False, allow_blank=True)

    class Meta:
        model = PRODUCT
        fields = '__all__'

class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = CART
        fields = '__all__'

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile  # your UserProfile model
        fields = '__all__'

class UserSerializer(serializers.ModelSerializer):
    userprofile = UserProfileSerializer(read_only=True)

    class Meta:
        model = User
        fields = [
            'id', 'username', 'first_name', 'last_name', 'email', 
            'is_staff', 'is_active', 'date_joined', 'userprofile'
        ]