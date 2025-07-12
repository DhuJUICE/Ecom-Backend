from rest_framework import serializers
from product_management.models import PRODUCT
from browse_management.models import MENU
from cart_management.models import CART
from checkout_management.models import TRANSACTION_LOG
from django.contrib.auth.models import User

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

#custom serializer to add a field to the returned data from token endpoint
class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)

        # Add custom fields to the response data
        data['is_staff'] = self.user.is_staff

        return data

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = PRODUCT
        fields = '__all__'

class MenuSerializer(serializers.ModelSerializer):
    class Meta:
        model = MENU
        fields = '__all__'

class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = CART
        fields = '__all__'

class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = TRANSACTION_LOG
        fields = '__all__'

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'